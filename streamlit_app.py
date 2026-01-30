import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# CSS ΣΥΜΠΥΚΝΩΜΕΝΟ & ΔΙΟΡΘΩΣΕΙΣ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .stApp { background-color: #f0f7ff; }
    
    /* 1. Μείωση κενού κάτω από το Χρόνο/Προσπάθειες */
    div[data-testid="stMetricSimpleValue"] { line-height: 1 !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) { margin-bottom: -25px !important; }

    /* 2. Στυλ Καρτών & Κουμπιών */
    .big-card { width: 100%; height: 130px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 20px; font-weight: bold; box-shadow: 0 6px 12px rgba(0,0,0,0.1); border: 4px solid; text-align: center; margin-bottom: 5px; }
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 20px; text-shadow: 2px 2px #023e8a; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }
    .card-label { font-size: 11px; text-transform: uppercase; margin-top: 5px; opacity: 0.8; }
    
    /* 3. ΜΕΓΑΛΟ ΦΙΝΑΛΕ CSS */
    .finish-box {
        background-color: #e0f2fe;
        border: 6px solid #0077b6;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin-top: 40px;
        color: #0077b6;
        font-family: 'Fredoka One', cursive;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    div.stButton > button[kind="primary"] { background-color: #0077b6 !important; color: white !important; height: 70px !important; font-size: 24px !important; border-radius: 20px !important; font-weight: bold !important; width: 100% !important; margin-top: 20px !important; }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

if 'game_running' not in st.session_state: st.session_state.game_running = False
if 'finished' not in st.session_state: st.session_state.finished = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running and not st.session_state.finished:
    st.markdown("<h1 style='text-align: center; color: #0077b6; font-family: Fredoka One;'>BRAIN GAME</h1>", unsafe_allow_html=True)
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    if selected and st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
        all_pairs = []
        for n in selected:
            for i in range(1, 11): all_pairs.append((f"{n} x {i}", n * i))
        selected_pairs = random.sample(all_pairs, 6)
        deck = []
        for p in selected_pairs:
            deck.append({'content': p[0], 'value': p[1], 'type': 'q'})
            deck.append({'content': str(p[1]), 'value': p[1], 'type': 'a'})
        random.shuffle(deck)
        st.session_state.update({'deck': deck, 'matched_indices': [], 'flipped_indices': [], 'attempts': 0, 'start_time': time.time(), 'game_running': True, 'finished': False})
        st.rerun()

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
elif st.session_state.game_running:
    elapsed = time.time() - st.session_state.start_time
    c1, c2 = st.columns(2)
    c1.metric("⏱️ Χρόνος", format_time(elapsed))
    c2.metric("🔄 Προσπάθειες", st.session_state.attempts)
    
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            is_matched = idx in st.session_state.matched_indices
            is_flipped = idx in st.session_state.flipped_indices or is_matched
            style = "card-matched" if is_matched else ("card-question" if is_flipped and card['type']=='q' else ("card-answer" if is_flipped else "card-closed"))
            content = card['content'] if is_flipped else "BRAIN<br>GAME"
            label = ("ΣΩΣΤΟ! ✅" if is_matched else ("ΠΡΑΞΗ" if card['type']=='q' else "ΑΠΟΤΕΛΕΣΜΑ")) if is_flipped else ""
            
            with cols[col]:
                st.markdown(f'<div class="big-card {style}"><div>{content}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                if st.button("ΠΑΤΑ", key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices)>=2, use_container_width=True):
                    st.session_state.flipped_indices.append(idx)
                    st.rerun()

    if len(st.session_state.flipped_indices) == 2:
        st.session_state.attempts += 1
        i1, i2 = st.session_state.flipped_indices
        if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
            st.session_state.matched_indices.extend([i1, i2])
        else: time.sleep(1.0)
        st.session_state.flipped_indices = []
        st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.final_stats = {'time': format_time(elapsed), 'attempts': st.session_state.attempts}
        st.session_state.game_running = False
        st.session_state.finished = True
        st.rerun()

# --- ΜΕΓΑΛΟ ΦΙΝΑΛΕ (ΞΕΧΩΡΙΣΤΗ ΣΕΛΙΔΑ) ---
elif st.session_state.finished:
    st.balloons()
    st.markdown(f"""
        <div class="finish-box">
            <h1 style='font-size: 50px; margin-bottom: 0px;'>🎉 Μπράβο!</h1>
            <h2 style='font-size: 30px; margin-top: 0px;'>Τα κατάφερες.</h2>
            <hr style='border: 1px solid #0077b6; opacity: 0.1; margin: 25px 0;'>
            <p style='font-size: 35px;'>⏱️ Χρόνος: {st.session_state.final_stats['time']}</p>
            <p style='font-size: 25px;'>🔄 Προσπάθειες: {st.session_state.final_stats['attempts']}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary"):
        st.session_state.finished = False
        st.rerun()
