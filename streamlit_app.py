import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Brain Game", page_icon="🧠", layout="centered")

# 2. CSS για 4x3 Grid, Touch-friendly κάρτες και UI
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* 4 Στήλες για το Grid */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .main-card {
        aspect-ratio: 1 / 1;
        perspective: 1000px;
        position: relative;
    }

    .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    .is-flipped { transform: rotateY(360deg); }

    .card-front, .card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 3px solid;
    }

    /* Πίσω πλευρά (Κλειστή κάρτα) */
    .card-back {
        background-color: #ced4da;
        color: #495057;
        border-color: #adb5bd;
        font-size: 40px;
    }

    /* Μπροστινή πλευρά (Ανοιχτή κάρτα) */
    .white-card { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 22px; }
    .blue-card { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 26px; }
    .matched-card { background-color: #d1ffdb !important; border-color: #4caf50 !important; color: #1b5e20 !important; }

    .hint-label { font-size: 10px; text-transform: uppercase; margin-top: 4px; opacity: 0.7; }

    /* Αόρατο κουμπί που καλύπτει όλη την κάρτα για Touch */
    .stButton > button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
        cursor: pointer;
    }
    
    /* Στυλ για το κουμπί ΞΕΚΙΝΑΜΕ (ίδιο με το προηγούμενο app) */
    .start-btn-style {
        background-color: #0077b6 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Helper Functions
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def init_game(selected_numbers):
    all_pairs = []
    for n in selected_numbers:
        for i in range(1, 11):
            all_pairs.append((f"{n} x {i}", n * i))
    
    selected_pairs = random.sample(all_pairs, 6)
    deck = []
    for pair in selected_pairs:
        deck.append({'content': pair[0], 'value': pair[1], 'type': 'q'}) # Λευκή
        deck.append({'content': str(pair[1]), 'value': pair[1], 'type': 'a'}) # Γαλάζια
    
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.game_running = True
    st.session_state.matched_indices = []
    st.session_state.flipped_indices = []
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.finish_time = None

# 4. Logic & Session State
if 'deck' not in st.session_state:
    st.session_state.deck = []
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.title("🧮 Multiplication Brain Game")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", use_container_width=True, type="primary"):
            init_game(selected)
            st.rerun()

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
else:
    elapsed = int(time.time() - st.session_state.start_time) if not st.session_state.finish_time else st.session_state.finish_time
    
    # Progress Bar & Stats
    progress = len(st.session_state.matched_indices) / 12
    st.progress(progress)
    
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
            
            flipped_class = "is-flipped" if is_flipped else ""
            
            if is_matched:
                card_class, content, label = "matched-card", "✅", "ΒΡΕΘΗΚΕ"
            elif is_flipped:
                if card['type'] == 'q':
                    card_class, label = "white-card", "ΠΡΑΞΗ 📝"
                else:
                    card_class, label = "blue-card", "ΑΠΟΤΕΛΕΣΜΑ 🎯"
                content = card['content']
            else:
                card_class, content, label = "card-back", "❓", ""

            card_html = f"""
            <div class="main-card">
                <div class="card-inner {flipped_class}">
                    <div class="card-back">❓</div>
                    <div class="card-front {card_class}">
                        <div>{content}</div>
                        <div class="hint-label">{label}</div>
                    </div>
                </div>
            </div>
            """
            with cols[col]:
                st.markdown(card_html, unsafe_allow_html=True)
                if not is_flipped and len(st.session_state.flipped_indices) < 2:
                    if st.button("", key=f"card_{idx}"):
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
            time.sleep(0.6)
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Μπράβο! Το ολοκλήρωσες σε {format_time(elapsed)} με {st.session_state.attempts} προσπάθειες!")
        if st.button("🔄 Παίξε Ξανά", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
