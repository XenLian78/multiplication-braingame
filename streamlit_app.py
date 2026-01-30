import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game", page_icon="🧠", layout="centered")

# --- CSS SECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { display: none; }
    .stApp { background-color: #f0f7ff; }
    
    /* Σταθεροποίηση Metrics */
    [data-testid="stMetricContainer"] { 
        background: white; padding: 10px; border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Σταθερό Ύψος Καρτών για να μην αλλάζουν θέση */
    .card-wrapper {
        margin-bottom: 45px; /* Το κενό που καταλαμβάνει το κουμπί ΚΛΙΚ */
    }

    .big-card { 
        width: 100%; height: 110px; display: flex; flex-direction: column; 
        align-items: center; justify-content: center; border-radius: 15px; 
        font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        border: 3px solid; text-align: center;
    }
    
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 16px; text-shadow: 1px 1px #023e8a; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 22px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 26px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 22px; }
    .card-label { font-size: 9px; text-transform: uppercase; margin-top: 2px; opacity: 0.7; }

    /* Countdown Box */
    .countdown-box {
        text-align: center; color: #d62828; font-family: 'Fredoka One', cursive; font-size: 20px;
        margin-bottom: 20px; padding: 15px; background-color: white;
        border-radius: 15px; border: 3px dashed #d62828;
    }

    /* Μπλε Κουμπιά (Flat Style) */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }

    /* Reset Button */
    .reset-btn div.stButton > button {
        background-color: #ffb703 !important; color: #023e8a !important;
        border: none !important; border-radius: 10px !important;
        font-weight: bold !important; height: 45px !important;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

# --- STATE ---
if 'game_running' not in st.session_state: st.session_state.game_running = False
if 'show_finish' not in st.session_state: st.session_state.show_finish = False
if 'memory_mode' not in st.session_state: st.session_state.memory_mode = False

# --- 1. ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running and not st.session_state.show_finish:
    st.title("🧠 Brain Game: Προπαίδεια")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"s_{i}")]
    
    st.write("---")
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
            all_pairs = []
            for n in selected:
                for i in range(1, 11): all_pairs.append((f"{n} x {i}", n * i))
            
            selected_pairs = random.sample(all_pairs, 6)
            deck = []
            for p in selected_pairs:
                deck.append({'content': p[0], 'value': p[1], 'type': 'q'})
                deck.append({'content': str(p[1]), 'value': p[1], 'type': 'a'})
            random.shuffle(deck)
            
            st.session_state.update({
                'deck': deck, 'matched_indices': [], 'flipped_indices': [], 
                'attempts': 0, 'game_running': True, 'memory_mode': True, 
                'memory_start': time.time(), 'start_time': None
            })
            st.rerun()

# --- 2. ΚΥΡΙΩΣ ΠΑΙΧΝΙΔΙ ---
elif st.session_state.game_running:
    if st.session_state.memory_mode:
        time_left = 15 - int(time.time() - st.session_state.memory_start) # 15 δευτερόλεπτα
        if time_left <= 0:
            st.session_state.memory_mode = False
            st.session_state.start_time = time.time()
            st.rerun()
        st.markdown(f'<div class="countdown-box">👀 Απομνημόνευσε τις θέσεις!<br>Κλείνουν σε: {max(0, time_left)}</div>', unsafe_allow_html=True)
    else:
        elapsed = time.time() - st.session_state.start_time
        c1, c2, c3 = st.columns([1, 1, 1])
        c1.metric("⏱️ Χρόνος", format_time(elapsed))
        c2.metric("🔄 Προσπάθειες", st.session_state.attempts)
        with c3:
            st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
            if st.button("🔄 ΑΛΛΑΓΗ"):
                st.session_state.game_running = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.write("") 

    # Πλέγμα
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            is_m, is_f = idx in st.session_state.matched_indices, idx in st.session_state.flipped_indices
            show = st.session_state.memory_mode or is_f or is_m
            
            if is_m:
                style, content = "card-matched", f'<div>{card["content"]}</div><div class="card-label">ΣΩΣΤΟ! ✅</div>'
            elif show:
                style = "card-question" if card['type'] == 'q' else "card-answer"
                label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"
                content = f'<div>{card["content"]}</div><div class="card-label">{label}</div>'
            else:
                style, content = "card-closed", '<div class="brain-text">BRAIN<br>GAME</div>'
            
            with cols[col]:
                # Χρήση wrapper για σταθερό κενό
                st.markdown(f'<div class="card-wrapper"><div class="big-card {style}">{content}</div></div>', unsafe_allow_html=True)
                
                # Εμφάνιση κουμπιού μόνο αν ΔΕΝ είμαστε σε memory mode
                if not st.session_state.memory_mode and not (is_f or is_m):
                    # Μετακίνηση του κουμπιού "πάνω" στο κενό του wrapper
                    st.markdown('<style>div[key="btn_'+str(idx)+'"] { margin-top: -40px; }</style>', unsafe_allow_html=True)
                    if st.button("ΚΛΙΚ", key=f"btn_{idx}", use_container_width=True):
                        if len(st.session_state.flipped_indices) < 2:
                            st.session_state.flipped_indices.append(idx)
                            st.rerun()

    # Logic
    if not st.session_state.memory_mode and len(st.session_state.flipped_indices) == 2:
        st.session_state.attempts += 1
        i1, i2 = st.session_state.flipped_indices
        if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
            st.session_state.matched_indices.extend([i1, i2])
            st.session_state.flipped_indices = []
            time.sleep(0.4)
            st.rerun()
        else:
            time.sleep(0.8)
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = time.time() - st.session_state.start_time
        st.session_state.game_running, st.session_state.show_finish = False, True
        st.rerun()
    
    if st.session_state.memory_mode:
        time.sleep(0.5)
        st.rerun()

# --- 3. ΤΕΛΙΚΗ ΟΘΟΝΗ ---
elif st.session_state.show_finish:
    st.balloons()
    st.markdown(f"""
        <div style="background-color: white; border-radius: 25px; padding: 40px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <h1 style="color: #0077b6; font-family: 'Fredoka One';">🏆 Φανταστικά!</h1>
            <p style="font-size: 22px; color: #495057;">Ολοκλήρωσες την πρόκληση σε:</p>
            <h2 style="color: #00b4d8; font-size: 45px;">{format_time(st.session_state.finish_time)}</h2>
            <p style="font-size: 18px; color: #6c757d;">Συνολικές προσπάθειες: <b>{st.session_state.attempts}</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", use_container_width=True):
        st.session_state.show_finish = False
        st.rerun()
