import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας (Πρέπει να είναι η πρώτη εντολή)
st.set_page_config(page_title="Brain Game", page_icon="🧠", layout="centered")

# 2. ΑΠΟΛΥΤΟ CSS ΓΙΑ MARGINS ΚΑΙ ΚΟΥΜΠΙΑ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Εξαφάνιση όλων των κενών στην κορυφή */
    .stApp { margin-top: -80px !important; background-color: #f0f7ff; }
    header {visibility: hidden !important;}
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    
    /* Μείωση κενού ανάμεσα στα στοιχεία */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }

    /* ΓΙΓΑΝΤΙΑ ΚΟΥΜΠΙΑ ΞΕΚΙΝΑΜΕ & ΠΑΙΞΕ ΞΑΝΑ */
    button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 100px !important; /* Πάρα πολύ μεγάλο ύψος */
        font-size: 40px !important; /* Τεράστια γράμματα */
        border-radius: 25px !important;
        width: 100% !important;
        display: block !important;
        box-shadow: 0 10px 20px rgba(0,119,182,0.4) !important;
        border: none !important;
        cursor: pointer !important;
    }

    /* Σταθερότητα Καρτών */
    [data-testid="stColumn"] { min-height: 170px !important; }

    .big-card {
        width: 100%; height: 120px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border-radius: 20px; font-weight: bold; border: 4px solid;
        text-align: center; margin-bottom: 5px;
    }

    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 22px; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 28px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 32px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 28px; }
    .card-label { font-size: 11px; text-transform: uppercase; margin-top: 5px; opacity: 0.8; }

    /* Πλαίσιο Φινάλε */
    .finish-box {
        background-color: #e0f2fe; border: 8px solid #0077b6; border-radius: 30px;
        padding: 40px; text-align: center; color: #0077b6; font-family: 'Fredoka One', cursive;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

# Αρχικοποίηση Session State
if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.markdown("<h1 style='text-align: center; color: #0077b6; font-family: Fredoka One;'>BRAIN GAME</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Διάλεξε προπαίδεια:</h3>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    st.write(" ") # Μικρό κενό
    
    if len(selected) > 0:
        # Το κουμπί ΞΕΚΙΝΑΜΕ
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", key="start_btn"):
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
            st.session_state.game_running = True
            st.rerun()
    else:
        st.warning("⚠️ Παρακαλώ επίλεξε τουλάχιστον έναν αριθμό!")

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
else:
    current_time = time.time()
    elapsed = current_time - st.session_state.start_time
    
    if len(st.session_state.matched_indices) < 12:
        m1, m2 = st.columns(2)
        m1.metric("⏱️ Χρόνος", format_time(elapsed))
        m2.metric("🔄 Προσπάθειες", st.session_state.attempts)

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
                    label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"
                    content = card['content']
                else:
                    style, content, label = "card-closed", "BRAIN<br>GAME", ""

                with cols[col]:
                    st.markdown(f'<div class="big-card {style}"><div class="{"brain-text" if style=="card-closed" else ""}">{content}</div><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
                    if not is_flipped and len(st.session_state.flipped_indices) < 2:
                        if st.button("ΚΛΙΚ", key=f"btn_{idx}", use_container_width=True):
                            st.session_state.flipped_indices.append(idx)
                            st.rerun()
                    else:
                        st.button("---", key=f"dis_{idx}", disabled=True, use_container_width=True)

        if len(st.session_state.flipped_indices) == 2:
            st.session_state.attempts += 1
            i1, i2 = st.session_state.flipped_indices
            if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
                st.session_state.matched_indices.extend([i1, i2])
                st.session_state.flipped_indices = []
                st.rerun()
            else:
                time.sleep(1.0)
                st.session_state.flipped_indices = []
                st.rerun()
    
    # ΦΙΝΑΛΕ
    else:
        st.balloons()
        st.markdown(f"""
            <div class="finish-box">
                <h1 style='font-size: 60px;'>🎉 Μπράβο!</h1>
                <p style='font-size: 40px;'>Τα κατάφερες!</p>
                <p style='font-size: 35px;'>⏱️ Χρόνος: {format_time(elapsed)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", key="reset_btn"):
            st.session_state.game_running = False
            st.rerun()
