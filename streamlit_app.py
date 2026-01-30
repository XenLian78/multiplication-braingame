import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για την εμφάνιση (Διορθωμένο για να παίζει παντού)
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Μεγάλο Μπλε Κουμπί ΞΕΚΙΝΑΜΕ */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 65px !important;
        font-size: 26px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        width: 100%;
    }

    /* Στυλ Κάρτας - Μεγαλύτερες */
    .big-card {
        width: 100%;
        height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Χρώματα */
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 28px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 32px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 28px; }

    .card-label { font-size: 12px; text-transform: uppercase; margin-top: 10px; font-weight: normal; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.title("🧠 Brain Game: Προπαίδεια")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if not selected:
        st.info("ℹ️ Επίλεξε τουλάχιστον έναν αριθμό για να ξεκινήσεις!")
    else:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
            all_pairs = []
            for n in selected:
                for i in range(1, 11):
                    all_pairs.append((f"{n} x {i}", n * i))
            
            selected_pairs = random.sample(all_pairs, 6)
            deck = []
            for pair in selected_pairs:
                deck.append({'content': pair[0], 'value': pair[1], 'type': 'q'})
                deck.append({'content': str(pair[1]), 'value': pair[1], 'type': 'a'})
            
            random.shuffle(deck)
            st.session_state.deck = deck
            st.session_state.matched_indices = []
            st.session_state.flipped_indices = []
            st.session_state.attempts = 0
            st.session_state.start_time = time.time()
            st.session_state.finish_time = None
            st.session_state.game_running = True
            st.rerun()

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
else:
    elapsed = time.time() - st.session_state.start_time if not st.session_state.finish_time else st.session_state.finish_time
    
    c1, c2 = st.columns(2)
    c1.metric("⏱️ Χρόνος", format_time(elapsed))
    c2.metric("🔄 Προσπάθειες", st.session_state.attempts)

    # Grid 4x3
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            is_matched = idx in st.session_state.matched_indices
            is_flipped = idx in st.session_state.flipped_indices or is_matched
            
            if is_matched:
                style, content, label = "card-matched", card['content'], "ΣΩΣΤΟ! ✅"
            elif is_flipped:
                style = "card-question" if card['type'] == 'q' else "card-answer"
                content, label = card['content'], ("ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ")
            else:
                style, content, label = "card-closed", "BRAIN", "GAME"

            with cols[col]:
                st.markdown(f'<div class="big-card {style}"><div>{content}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                
                # Κουμπί
                if not is_flipped and len(st.session_state.flipped_indices) < 2:
                    if st.button("ΠΑΤΑ ΕΔΩ", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.flipped_indices.append(idx)
                        st.rerun()

    # Match Logic
    if len(st.session_state.flipped_indices) == 2:
        st.session_state.attempts += 1
        i1, i2 = st.session_state.flipped_indices
        if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
            st.session_state.matched_indices.extend([i1, i2])
            st.session_state.flipped_indices = []
            st.rerun()
        else:
            time.sleep(1.2)
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Μπράβο! Χρόνος: {format_time(elapsed)} | Προσπάθειες: {st.session_state.attempts}")
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary"):
            st.session_state.game_running = False
            st.rerun()
