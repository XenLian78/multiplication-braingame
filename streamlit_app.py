import streamlit as st

import random

import time



# 1. Ρύθμιση σελίδας

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")



# 2. CSS για Σταθερότητα και Εμφάνιση

st.markdown("""

<style>

    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');



    .stApp { background-color: #f0f7ff; }

    

    /* Μεγάλο Μπλε Κουμπί ΞΕΚΙΝΑΜΕ */

    div.stButton > button[kind="primary"] {

        background-color: #0077b6 !important;

        color: white !important;

        height: 65px !important;

        font-size: 26px !important;

        border-radius: 15px !important;

        font-weight: bold !important;

    }



    /* Σταθερό Κοντέινερ για να μην κουνιούνται οι κάρτες */

    [data-testid="stColumn"] {

        min-height: 220px !important;

        display: flex;

        flex-direction: column;

        justify-content: flex-start;

    }



    /* Στυλ Κάρτας */

    .big-card {

        width: 100%;

        height: 140px;

        display: flex;

        flex-direction: column;

        align-items: center;

        justify-content: center;

        border-radius: 20px;

        font-weight: bold;

        box-shadow: 0 6px 12px rgba(0,0,0,0.1);

        border: 4px solid;

        text-align: center;

        margin-bottom: 10px;

        transition: all 0.3s ease;

    }



    /* Κλειστή Κάρτα */

    .card-closed { 

        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); 

        color: white; 

        border-color: #023e8a; 

    }

    

    .brain-text {

        font-family: 'Fredoka One', cursive;

        font-size: 22px;

        letter-spacing: 2px;

        text-shadow: 2px 2px #023e8a;

    }



    /* Ανοιχτές κάρτες */

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

            

            if is_matched:

                style = "card-matched"

                content = f'<div>{card["content"]}</div><div class="card-label">ΣΩΣΤΟ! ✅</div>'

            elif is_flipped:

                style = "card-question" if card['type'] == 'q' else "card-answer"

                label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"

                content = f'<div>{card["content"]}</div><div class="card-label">{label}</div>'

            else:

                style = "card-closed"

                content = '<div class="brain-text">BRAIN<br>GAME</div>'



            with cols[col]:

                # Εμφάνιση Κάρτας

                st.markdown(f'<div class="big-card {style}">{content}</div>', unsafe_allow_html=True)

                

                # Κουμπί που δεν εξαφανίζεται αλλά απενεργοποιείται

                btn_label = "ΠΑΤΑ ΕΔΩ" if not is_flipped else "---"

                if st.button(btn_label, key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices) >= 2, use_container_width=True):

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

            time.sleep(1.2)

            st.session_state.flipped_indices = []

            st.rerun()



   # Φινάλε με το μεγάλο γαλάζιο πλαίσιο
    else:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.markdown(f"""
            <div class="finish-box">
                <h1 style='font-size: 50px;'>🎉 Μπράβο!</h1>
                <h2 style='font-size: 35px;'>Τα κατάφερες.</h2>
                <hr style='border: 1px solid #0077b6; opacity: 0.2; margin: 20px 0;'>
                <p style='font-size: 35px;'>⏱️ Χρόνος: {format_time(elapsed)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
