import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Memory Game", page_icon="🧠", layout="centered")

# 2. CSS για Μεγάλες Κάρτες και Καθαρό UI
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid;
        text-align: center;
        margin-bottom: 5px;
        font-size: 22px;
    }

    /* Χρώματα Καρτών */
    .card-closed { background-color: #ced4da; color: #495057; border-color: #adb5bd; font-size: 35px; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; }

    /* Ταμπέλα τύπου κάρτας (Πράξη/Αποτέλεσμα) */
    .card-hint { font-size: 10px; text-transform: uppercase; margin-top: 5px; font-weight: normal; }

    /* Μεγάλο Μπλε Κουμπί ΞΕΚΙΝΑΜΕ */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 60px !important;
        font-size: 24px !important;
        border-radius: 15px !important;
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
    st.title("🧮 Το Παιχνίδι της Προπαίδειας")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    st.divider()
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
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
    
    st.progress(len(st.session_state.matched_indices) / 12)
    
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
            
            # Επιλογή στυλ κάρτας
            if is_matched:
                style, content, hint = "card-matched", "✅", "ΣΩΣΤΟ!"
            elif is_flipped:
                if card['type'] == 'q':
                    style, content, hint = "card-question", card['content'], "ΠΡΑΞΗ 📝"
                else:
                    style, content, hint = "card-answer", card['content'], "ΑΠΟΤΕΛΕΣΜΑ 🎯"
            else:
                style, content, hint = "card-closed", "❓", ""

            with cols[col]:
                # Εμφάνιση Κάρτας
                st.markdown(f"""
                <div class="big-card {style}">
                    <div>
                        {content}
                        <div class="card-hint">{hint}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Κουμπί ελέγχου κάτω από την κάρτα
                button_disabled = is_flipped or len(st.session_state.flipped_indices) >= 2
                if st.button("ΠΑΤΑ ΕΔΩ", key=f"btn_{idx}", disabled=button_disabled, use_container_width=True):
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
            time.sleep(1.2) # Χρόνος για να προλάβουν να δουν την κάρτα
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Μπράβο! Το ολοκλήρωσες σε {format_time(elapsed)}!")
        if st.button("🔄 Παίξε Ξανά", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
