import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για την εξάλειψη των κενών και την εμφάνιση
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Μηδενισμός κενού στην κορυφή και απόκρυψη header */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -40px !important;
    }
    header {visibility: hidden;}
    
    /* Εξάλειψη κενών ανάμεσα στα στοιχεία */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    .stApp { background-color: #f0f7ff; }
    
    /* Μεγάλο Μπλε Κουμπί ΞΕΚΙΝΑΜΕ / ΠΑΙΞΕ ΞΑΝΑ */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 75px !important;
        font-size: 30px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(0,119,182,0.3) !important;
    }

    /* Σταθερό Κοντέινερ Καρτών */
    [data-testid="stColumn"] {
        min-height: 180px !important;
        padding: 2px !important;
    }

    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 125px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        font-weight: bold;
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 5px;
    }

    .card-closed { 
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); 
        color: white; 
        border-color: #023e8a; 
    }
    
    .brain-text {
        font-family: 'Fredoka One', cursive;
        font-size: 20px;
        line-height: 1.1;
    }

    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }

    .card-label { font-size: 11px; text-transform: uppercase; margin-top: 5px; opacity: 0.8; font-weight: normal; }

    /* Μικρότερα κουμπιά ελέγχου */
    div.stButton > button:not([kind="primary"]) {
        height: 35px !important;
        font-size: 14px !important;
        margin-top: 0px !important;
    }

    /* Το Μεγάλο Γαλάζιο Πλαίσιο Τέλους */
    .finish-box {
        background-color: #e0f2fe;
        border: 6px solid #0077b6;
        border-radius: 30px;
        padding: 35px;
        text-align: center;
        margin: 15px 0px;
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
    st.markdown("<h1 style='text-align: center; color: #0077b6;'>🧠 Brain Game</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Ποιους αριθμούς θα μάθουμε σήμερα;</h4>", unsafe_allow_html=True)
    
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
