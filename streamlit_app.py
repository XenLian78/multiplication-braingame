import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game", page_icon="🧠", layout="centered")

# --- ΚΑΘΑΡΟ CSS ΣΕ ΜΙΚΡΑ ΜΕΡΗ ---
st.markdown('<style>@import url("https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap");</style>', unsafe_allow_html=True)
st.markdown('<style>.block-container { padding-top: 0.5rem !important; }.stApp { background-color: #f0f7ff; }</style>', unsafe_allow_html=True)
st.markdown('<style>[data-testid="stHeader"] { display: none; }[data-testid="stMetricContainer"] { margin-top: -10px; margin-bottom: -35px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.big-card { width: 100%; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 18px; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 4px solid; text-align: center; margin-bottom: 2px; font-family: sans-serif; }</style>', unsafe_allow_html=True)
st.markdown('<style>.card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }.brain-text { font-family: "Fredoka One", cursive; font-size: 19px; text-shadow: 2px 2px #023e8a; }</style>', unsafe_allow_html=True)
st.markdown('<style>.card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }.card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }.card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.card-label { font-size: 10px; text-transform: uppercase; margin-top: 2px; font-weight: normal; opacity: 0.8; }.countdown-box { text-align: center; color: #d62828; font-family: "Fredoka One", cursive; font-size: 22px; margin-bottom: 15px; padding: 10px; background-color: rgba(214, 40, 40, 0.1); border-radius: 15px; border: 2px dashed #d62828; }</style>', unsafe_allow_html=True)
st.markdown('<style>div.stButton > button[kind="primary"] { background-color: #0077b6 !important; color: white !important; height: 60px !important; font-size: 24px !important; border-radius: 15px !important; }.reset-btn div.stButton > button { background-color: #ffb703 !important; color: #023e8a !important; height: 40px !important; border: 2px solid #fb8500 !important; }</style>', unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

# --- STATE ---
if 'game_running' not in st.session_state: st.session_state.game_running = False
if 'show_finish' not in st.session_state: st.session_state.show_finish = False
if 'memory_mode' not in st.session_state: st.session_state.memory_mode = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running and not st.session_state.show_finish:
    st.title("🧠 Brain Game: Προπαίδεια")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"s_{i}")]
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς!")
    elif st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
        all_pairs = []
        for n in selected:
            for i in range(1, 11): all_pairs.append((f"{n}x{i}", n * i))
        selected_pairs = random.sample(all_pairs, 6)
        deck = []
        for p in selected_pairs:
            deck.append({'content': p[0], 'value': p[1], 'type': 'q'})
            deck.append({'content': str(p[1]), 'value': p[1], 'type': 'a'})
        random.shuffle(deck)
        st.session_state.update({'deck': deck, 'matched_indices': [], 'flipped_indices': [], 'attempts': 0, 'game_running': True, 'memory_mode': True, 'memory_start': time.time()})
        st.rerun()

# --- ΚΕΝΤΡΙΚΟ ΠΑΙΧΝΙΔΙ ---
elif st.session_state.game_running:
    if st.session_state.memory_mode:
        time_left = 20 - int(time.time() - st.session_state.memory_start)
        if time_left <= 0:
            st.session_state.memory_mode = False
            st.session_state.start_time = time.time()
            st.rerun()
        st.markdown(f'<div class="countdown-box">👀
