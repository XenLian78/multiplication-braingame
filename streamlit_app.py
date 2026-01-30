import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Brain Game", page_icon="🧠", layout="centered")

# 2. CSS για το Memory Grid και το 360 Flip
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Grid Layout */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 10px;
    }
    
    /* Card Styles */
    .main-card {
        aspect-ratio: 1 / 1;
        perspective: 1000px;
        cursor: pointer;
    }

    .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    /* Το 360 Rotate που ζήτησες */
    .is-flipped { transform: rotateY(360deg); }

    .card-front, .card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid;
    }

    /* Πίσω πλευρά (Κλειστή κάρτα) */
    .card-back {
        background-color: #495057;
        color: white;
        border-color: #343a40;
    }

    /* Μπροστά πλευρά (Ανοιχτή κάρτα) */
    .white-card { background-color: white; color: #495057; border-color: #a2d2ff; }
    .blue-card { background-color: #f0f9ff; color: #0077b6; border-color: #00b4d8; }
    .matched-card { background-color: #d1ffdb !important; border-color: #4caf50 !important; color: #1b5e20 !important; }

    /* Stats Box */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 2px solid #bde0fe;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if 'deck' not in st.session_state:
    st.session_state.deck = []
    st.session_state.game_running = False
    st.session_state.flipped_indices = []
    st.session_state.matched_indices = []
    st.session_state.attempts = 0
    st.session_state.start_time = None
    st.session_state.finish_time = None

def init_game(selected_numbers):
    # Δημιουργούμε 6 τυχαία ζευγάρια
    all_pairs = []
    for n in selected_numbers:
        for i in range(1, 11):
            all_pairs.append((f"{n} x {i}", n * i))
    
    selected_pairs = random.sample(all_pairs, 6)
    
    deck = []
    for pair in selected_pairs:
        # Λευκή κάρτα (Ερώτηση)
        deck.append({'content': pair[0], 'value': pair[1], 'type': 'q'})
        # Γαλάζια κάρτα (Απάντηση)
        deck.append({'content': str(pair[1]), 'value': pair[1], 'type': 'a'})
    
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.game_running = True
    st.session_state.matched_indices = []
    st.session_state.flipped_indices = []
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.finish_time = None

# --- HOME PAGE ---
if not st.session_state.game_running:
    st.title("🧠 Multiplication Brain Game")
    st.subheader("Διάλεξε προπαίδεια για να ξεκινήσεις το Memory!")
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
        if selected:
            init_game(selected)
            st.rerun()
        else:
            st.warning("Επίλεξε τουλάχιστον έναν αριθμό!")

# --- GAME PAGE ---
else:
    # Υπολογισμός χρόνου
    current_time = int(time.time() - st.session_state.start_time) if not st.session_state.finish_time else st.session_state.finish_time
    
    st.markdown(f"""
        <div class="stats-container">
            <div>⏱️ Χρόνος: <b>{current_time}s</b></div>
            <div>🔄 Προσπάθειες: <b>{st.session_state.attempts}</b></div>
            <div>✅ Βρέθηκαν: <b>{len(st.session_state.matched_indices)//2} / 6</b></div>
        </div>
    """, unsafe_allow_html=True)

    # Έλεγχος αν τελείωσε το παιχνίδι
    if len(st.session_state.matched_indices) == 12:
        if not st.session_state.finish_time:
            st.session_state.finish_time = current_time
        st.balloons()
        st.success(f"Μπράβο! Το ολοκλήρωσες σε {st.session_state.finish_time} δευτερόλεπτα με {st.session_state.attempts} προσπάθειες!")
        if st.button("🔄 Παίξε ξανά", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
        st.stop()

    # Δημιουργία του Grid
    cols = st.columns(3)
    for idx, card in enumerate(st.session_state.deck):
        with cols[idx % 3]:
            is_flipped = idx in st.session_state.flipped_indices or idx in st.session_state.matched_indices
            flipped_class = "is-flipped" if is_flipped else ""
            
            # Επιλογή χρώματος
            if idx in st.session_state.matched_indices:
                card_class = "matched-card"
            elif card['type'] == 'q':
                card_class = "white-card"
            else:
                card_class = "blue-card"

            # HTML Card
            card_html = f"""
            <div class="main-card">
                <div class="card-inner {flipped_class}">
                    <div class="card-back">❓</div>
                    <div class="card-front {card_class}">{card['content']}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Button για το κλικ (αόρατο πάνω από την κάρτα)
            if not is_flipped and len(st.session_state.flipped_indices) < 2:
                if st.button("Κλικ", key=f"btn_{idx}", help="Άνοιξε την κάρτα", use_container_width=True):
                    st.session_state.flipped_indices.append(idx)
                    st.rerun()

    # Λογική αντιστοίχισης
    if len(st.session_state.flipped_indices) == 2:
        idx1, idx2 = st.session_state.flipped_indices
        card1, card2 = st.session_state.deck[idx1], st.session_state.deck[idx2]
        
        st.session_state.attempts += 1
        
        # Αν είναι σωστό ζευγάρι
        if card1['value'] == card2['value'] and card1['type'] != card2['type']:
            st.session_state.matched_indices.extend([idx1, idx2])
            st.session_state.flipped_indices = []
            st.rerun()
        else:
            # Αν είναι λάθος - "Κλείνουν γρήγορα" όπως ζήτησες
            time.sleep(0.8) 
            st.session_state.flipped_indices = []
            st.rerun()

    if st.button("⬅️ Αλλαγή Αριθμών"):
        st.session_state.game_running = False
        st.rerun()
