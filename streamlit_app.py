import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# CSS ΣΥΜΠΥΚΝΩΜΕΝΟ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .stApp { background-color: #f0f7ff; }
    div.stButton > button[kind="primary"] { background-color: #0077b6 !important; color: white !important; height: 65px !important; font-size: 26px !important; border-radius: 15px !important; font-weight: bold !important; }
    [data-testid="stColumn"] { min-height: 220px !important; display: flex; flex-direction: column; justify-content: flex-start; }
    .big-card { width: 100%; height: 140px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 20px; font-weight: bold; box-shadow: 0 6px 12px rgba(0,0,0,0.1); border: 4px solid; text-align: center; margin-bottom: 10px; transition: all 0.3s ease; }
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 22px; letter-spacing: 2px; text-shadow: 2px 2px #023e8a; }
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
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    elif st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
        all_pairs = []
        for n in selected:
            for i in range(1, 11): all_pairs.append((f"{n} x {i}", n * i))
        selected_pairs = random.sample(all_pairs, 6)
        deck = []
        for p in selected_pairs:
            deck.append({'content': p[0], 'value': p[1], 'type': 'q'})
            deck.append({'content': str(p[1]), 'value': p[1], 'type': 'a'})
        random.shuffle(deck)
        st.session_state.update({'deck': deck, 'matched_indices': [], 'flipped_indices': [], 'attempts': 0, 'start_time': time.time(), 'finish_time': None, 'game_running': True})
        st.rerun()

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
else:
    elapsed = time.time() - st.session_state.start_time if not st.session_state.finish_time else st.session_state.finish_time
    c1, c2 = st.columns(2)
    c1.metric("⏱️ Χρόνος", format_time(elapsed))
    c2.metric("🔄 Προσπάθειες", st.session_state.attempts)
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            matched, flipped = idx in st.session_state.matched_indices, idx in st.session_state.flipped_indices
            if matched:
                style, content = "card-matched", f'<div>{card["content"]}</div><div class="card-label">ΣΩΣΤΟ! ✅</div>'
            elif flipped or matched:
                style = "card-question" if card['type'] == 'q' else "card-answer"
                label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"
                content = f'<div>{card["content"]}</div><div class="card-label">{label}</div>'
            else:
                style, content = "card-closed", '<div class="brain-text">BRAIN<br>GAME</div>'
            with cols[col]:
                st.markdown(f'<div class="big-card {style}">{content}</div>', unsafe_allow_html=True)
                lbl = "ΠΑΤΑ ΕΔΩ" if not (flipped or matched) else "---"
                if st.button(lbl, key=f"b_{idx}", disabled=flipped or matched or len(st.session_state.flipped_indices) >= 2, use_container_width=True):
                    st.session_state.flipped_indices.append(idx)
                    st.rerun()
    if len(st.session_state.flipped_indices) == 2:
        st.session_state.attempts += 1
        i1, i2 = st.session_state.flipped_indices
        if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
            st.session_state.matched_indices.extend([i1, i2])
        else: time.sleep(1.2)
        st.session_state.flipped_indices = []
        st.rerun()
    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Μπράβο! Χρόνος: {format_time(elapsed)}")
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
