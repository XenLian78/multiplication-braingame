import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# CSS ΓΙΑ ΤΟ ROTATION ΚΑΙ ΤΟ ΚΕΝΤΡΙΚΟ ΠΑΙΧΝΙΔΙ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .block-container { padding-top: 0.5rem !important; }
    [data-testid="stHeader"] { display: none !important; }
    .stApp { background-color: #f0f7ff; }

    .card-container {
        perspective: 1000px;
        width: 100%;
        height: 120px;
        margin-bottom: 10px;
        position: relative;
    }

    .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    /* Rotation 360 μοίρες */
    .flipped { transform: rotateY(360deg); }

    .card-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        border: 4px solid;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .card-front {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%);
        color: white;
        border-color: #023e8a;
    }

    .card-back-q { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-back-a { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-back-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }

    .brain-text { font-family: 'Fredoka One', cursive; font-size: 19px; text-shadow: 2px 2px #023e8a; }
    .card-label { font-size: 10px; text-transform: uppercase; margin-top: 2px; opacity: 0.8; font-weight: normal; }

    /* Αόρατο κουμπί */
    .stButton > button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 120px;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
    }

    [data-testid="stMetricContainer"] { margin-top: -10px !important; margin-bottom: -35px !important; }
    
    .reset-btn div.stButton > button {
        background-color: #ffb703 !important; color: #023e8a !important;
        height: 40px !important; font-size: 14px !important;
        position: relative; z-index: 20; border: 2px solid #fb8500 !important;
    }

    .finish-box {
        background-color: #e0f2fe; border: 6px solid #0077b6;
        border-radius: 30px; padding: 40px; text-align: center;
        margin-top: 10px; color: #0077b6; font-family: 'Fredoka One', cursive;
    }
    
    div.stButton > button[kind="primary"] { 
        background-color: #0077b6 !important; color: white !important; 
        height: 60px !important; font-size: 24px !important; border-radius: 15px !important;
    }
    
    .countdown-text {
        font-family: 'Fredoka One', cursive;
        font-size: 24px;
        color: #d62828;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

# State Initialization
if 'game_running' not in st.session_state: st.session_state.game_running = False
if 'show_finish' not in st.session_state: st.session_state.show_finish = False
if 'memory_mode' not in st.session_state: st.session_state.memory_mode = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running and not st.session_state.show_finish:
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
        st.session_state.update({
            'deck': deck, 'matched_indices': [], 'flipped_indices': [], 
            'attempts': 0, 'start_time': time.time(), 'game_running': True, 
            'memory_mode': True, 'memory_start': time.time()
        })
        st.rerun()

# --- ΚΕΝΤΡΙΚΟ ΠΑΙΧΝΙΔΙ ---
elif st.session_state.game_running:
    # Διαχείριση Memory Mode (10 δευτερόλεπτα)
    if st.session_state.memory_mode:
        time_left = 10 - int(time.time() - st.session_state.memory_start)
        if time_left <= 0:
            st.session_state.memory_mode = False
            st.session_state.start_time = time.time() # Μηδενισμός χρόνου παιχνιδιού μετά το memory mode
            st.rerun()
        st.markdown(f'<div class="countdown-text">👀 Απομνημόνευσε τις θέσεις! Κλείνουν σε: {time_left}...</div>', unsafe_allow_html=True)
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

    st.markdown('<div style="margin-top:-15px;">', unsafe_allow_html=True)
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            is_matched = idx in st.session_state.matched_indices
            is_flipped = idx in st.session_state.flipped_indices
            
            # Στο Memory Mode όλες οι κάρτες φαίνονται flipped
            show_content = st.session_state.memory_mode or is_flipped or is_matched
            flip_class = "flipped" if show_content else ""
            
            if is_matched:
                back_style = "card-back-matched"
                content = f'<div>{card["content"]}</div><div class="card-label">ΣΩΣΤΟ! ✅</div>'
            else:
                back_style = "card-back-q" if card['type'] == 'q' else "card-back-a"
                label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"
                content = f'<div>{card["content"]}</div><div class="card-label">{label}</div>'

            with cols[col]:
                st.markdown(f"""
                <div class="card-container">
                    <div class="card-inner {flip_class}">
                        <div class="card-face card-front">
                            <div class="brain-text">BRAIN<br>GAME</div>
                        </div>
                        <div class="card-face {back_style}">
                            {content}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Απενεργοποίηση κλικ κατά το Memory Mode
                if not st.session_state.memory_mode:
                    if st.button("", key=f"btn_{idx}", disabled=is_flipped or is_matched or len(st.session_state.flipped_indices) >= 2):
                        st.session_state.flipped_indices.append(idx)
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Λογική ελέγχου (μόνο αν δεν είμαστε σε memory mode)
    if not st.session_state.memory_mode:
        if len(st.session_state.flipped_indices) == 2:
            st.session_state.attempts += 1
            i1, i2 = st.session_state.flipped_indices
            if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
                st.session_state.matched_indices.extend([i1, i2])
            else:
                time.sleep(1.0)
            st.session_state.flipped_indices = []
            st.rerun()

        if len(st.session_state.matched_indices) == 12:
            st.session_state.finish_time = elapsed
            st.session_state.game_running = False
            st.session_state.show_finish = True
            st.rerun()
            
    # Αυτόματη ανανέωση για τον countdown
    if st.session_state.memory_mode:
        time.sleep(1)
        st.rerun()

# --- ΜΕΓΑΛΟ ΦΙΝΑΛΕ --- (Παραμένει ίδιο)
elif st.session_state.show_finish:
    st.balloons()
    st.markdown(f"""
        <div class="finish-box">
            <h1 style='font-size: 50px; margin-bottom: 0px;'>🎉 Μπράβο!</h1>
            <h2 style='font-size: 30px; margin-top: 0px;'>Τα κατάφερες.</h2>
            <hr style='border: 1px solid #0077b6; opacity: 0.1; margin: 25px 0;'>
            <p style='font-size: 35px;'>⏱️ Χρόνος: {format_time(st.session_state.finish_time)}</p>
            <p style='font-size: 25px;'>🔄 Προσπάθειες: {st.session_state.attempts}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
    if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", use_container_width=True):
        st.session_state.show_finish = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
