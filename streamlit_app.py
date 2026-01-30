import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game", page_icon="🧠", layout="centered")

# CSS για σταθερότητα
st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
    [data-testid="stHeader"] { display: none; }
    .stApp { background-color: #f0f7ff; }
    .card-slot { height: 180px; display: flex; flex-direction: column; margin-bottom: 10px; }
    .big-card { 
        width: 100%; height: 115px; display: flex; flex-direction: column; 
        align-items: center; justify-content: center; border-radius: 15px; 
        font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 3px solid; text-align: center;
    }
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 20px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 24px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 20px; }
    .click-spacer { height: 50px; margin-top: 8px; }
    /* Μπλε Flat Κουμπιά */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important; color: white !important; border: none !important;
        height: 55px !important; border-radius: 12px !important; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Κύριο Container που καθαρίζει τα πάντα
main_container = st.empty()

if 'page' not in st.session_state: st.session_state.page = "START"

# --- ΣΕΛΙΔΑ ΕΝΑΡΞΗΣ ---
if st.session_state.page == "START":
    with main_container.container():
        st.title("🧠 Brain Game: Προπαίδεια")
        st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
        cols = st.columns(5)
        selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
        
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True) and selected:
            all_pairs = []
            for n in selected:
                for i in range(1, 11): all_pairs.append((f"{n} x {i}", n * i))
            
            selected_pairs = random.sample(all_pairs, 6)
            deck = []
            for p in selected_pairs:
                deck.append({'content': p[0], 'value': p[1], 'type': 'q'})
                deck.append({'content': str(p[1]), 'value': p[1], 'type': 'a'})
            random.shuffle(deck)
            
            st.session_state.update({'deck': deck, 'matched_indices': [], 'flipped_indices': [], 'attempts': 0, 'page': "GAME", 'memory_mode': True, 'memory_start': time.time()})
            main_container.empty() # ΕΔΩ ΓΙΝΕΤΑΙ ΤΟ ΜΑΓΙΚΟ: Σβήνει τα πάντα πριν το rerun
            st.rerun()

# --- ΣΕΛΙΔΑ ΠΑΙΧΝΙΔΙΟΥ ---
elif st.session_state.page == "GAME":
    with main_container.container():
        if st.session_state.memory_mode:
            time_left = 15 - int(time.time() - st.session_state.memory_start)
            if time_left <= 0:
                st.session_state.memory_mode, st.session_state.start_time = False, time.time()
                st.rerun()
            st.warning(f"👀 Απομνημόνευσε! Κλείνουν σε: {time_left}")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("⏱️ Χρόνος", int(time.time() - st.session_state.start_time))
            c2.metric("🔄 Προσπάθειες", st.session_state.attempts)
            if c3.button("🔄 ΑΛΛΑΓΗ"):
                st.session_state.page = "START"
                main_container.empty()
                st.rerun()

        # Grid
        for row in range(3):
            grid_cols = st.columns(4)
            for col in range(4):
                idx = row * 4 + col
                card = st.session_state.deck[idx]
                is_m, is_f = idx in st.session_state.matched_indices, idx in st.session_state.flipped_indices
                show = st.session_state.memory_mode or is_f or is_m
                
                style = "card-matched" if is_m else ("card-question" if show and card['type']=='q' else ("card-answer" if show else "card-closed"))
                content = card['content'] if show else "BRAIN GAME"
                
                with grid_cols[col]:
                    st.markdown(f'<div class="card-slot"><div class="big-card {style}">{content}</div>', unsafe_allow_html=True)
                    if not st.session_state.memory_mode and not (is_f or is_m):
                        if st.button("ΚΛΙΚ", key=f"btn_{idx}", use_container_width=True):
                            if len(st.session_state.flipped_indices) < 2:
                                st.session_state.flipped_indices.append(idx)
                                st.rerun()
                    else: st.markdown('<div class="click-spacer"></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # Logic για το Memory Mode ανανέωση
        if st.session_state.memory_mode:
            time.sleep(1)
            st.rerun()

        # Matching Logic
        if len(st.session_state.flipped_indices) == 2:
            st.session_state.attempts += 1
            i1, i2 = st.session_state.flipped_indices
            if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
                st.session_state.matched_indices.extend([i1, i2])
            time.sleep(0.6)
            st.session_state.flipped_indices = []
            st.rerun()

        if len(st.session_state.matched_indices) == 12:
            st.session_state.page = "START" # Ή "FINISH"
            st.balloons()
            time.sleep(2)
            st.rerun()
