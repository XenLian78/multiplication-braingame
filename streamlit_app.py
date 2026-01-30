import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας - Force narrow layout για να μην απλώνει
st.set_page_config(page_title="Brain Game", page_icon="🧠", layout="centered")

# 2. CSS για Συμπύκνωση και Διόρθωση Θέσης
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Αφαίρεση κενών στην κορυφή */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    .stApp { background-color: #f0f7ff; }
    
    /* Συμπύκνωση Checkboxes */
    div[data-testid="stCheckbox"] {
        margin-bottom: -15px !important;
    }

    /* Μεγάλα Κουμπιά */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 70px !important;
        font-size: 28px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 10px !important;
    }

    /* Σταθερό Κοντέινερ Καρτών */
    [data-testid="stColumn"] {
        min-height: 200px !important;
    }

    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 5px;
    }

    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 20px; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }
    .card-label { font-size: 11px; text-transform: uppercase; margin-top: 5px; font-weight: normal; opacity: 0.8; }

    /* Πλαίσιο Τέλους */
    .finish-box {
        background-color: #e0f2fe;
        border: 5px solid #0077b6;
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        color: #0077b6;
        font-family: 'Fredoka One', cursive;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.title("🧠 Brain Game")
    st.markdown("#### Ποια προπαίδεια θα παίξουμε;")
    
    # Πιο μαζεμένο grid για τους αριθμούς
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς!")
    else:
        # Το κουμπί τώρα θα είναι ακριβώς κάτω από τους αριθμούς
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
    
    if len(st.session_state.matched_indices) < 12:
        c1, c2 = st.columns(2)
        c1.metric("⏱️ Χρόνος", format_time(elapsed))
        c2.metric("🔄 Προσπάθειες", st.session_state.attempts)

        for row in range(3):
            cols = st.columns(4)
            for col in range(4):
                idx = row * 4 + col
                card = st.session_state.deck[idx]
                is_matched = idx in st.session_state.matched_indices
                is_flipped = idx in st.session_state.flipped
