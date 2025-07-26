
import streamlit as st

pages = {
    "🏠 Home": [
        st.Page("Home.py", title="Home", icon=":material/home:"),
    ],
    " 📺 Query Support": [
        st.Page("pages/Bot.py", title="Talk to Shweta", icon=":material/chat:"),
        st.Page("pages/main.py", title="YouTube Q&A", icon=":material/smart_display:"),
        st.Page("pages/Youtube_summarizer.py", title="YouTube Vid Summary", icon=":material/video_library:"),
        
    ],
    "📄 Doc Support": [
        st.Page("pages/pdf_summarizer.py", title="PDF Support", icon=":material/description:"),
        st.Page("pages/grammer.py", title="Grammer Checker", icon=":material/edit:"),
        st.Page("pages/DocumentTranslator.py", title="Document Translator", icon=":material/translate:"),
        st.Page("pages/Flash_card.py", title="FlashCard Generator", icon=":material/card_travel:"),
    ],
    " 🎮 Fun Zone": [
        st.Page("pages/random_game.py", title="Guess the Number", icon=":material/casino:"),
        st.Page("pages/tic_tac_toe.py", title="Tic Tac Toe", icon=":material/games:"),
    ],
    " 👤 Account": [
        st.Page("pages/feedback.py", title="Feedback", icon=":material/feedback:"),
        st.Page("pages/contact_us.py", title="Contact Us", icon=":material/contact_mail:"),
        st.Page("pages/terms.py", title="Terms of Service", icon=":material/gavel:"),
    ]
}

pages1 = {
    
    " 🏠 Home ": [
        st.Page("Home.py", title="Home", icon=":material/home:"),
    ],
    " 📺 Query Support": [
        st.Page("pages/Bot.py", title="Talk to Shweta", icon=":material/chat:"),
        st.Page("pages/main.py", title="YouTube Q&A", icon=":material/smart_display:"),
        st.Page("pages/Youtube_summarizer.py", title="YouTube Vid Summary", icon=":material/video_library:"),
    ],
    " 📄 Doc Support": [
        st.Page("pages/pdf_summarizer.py", title="PDF Support", icon=":material/description:"),
        st.Page("pages/grammer.py", title="Grammer Checker", icon=":material/edit:"),
        st.Page("pages/DocumentTranslator.py", title="Document Translator", icon=":material/translate:"),
        st.Page("pages/Flash_card.py", title="FlashCard Generator", icon=":material/card_travel:"),
    ],
    " 🎮 Fun Zone": [
        st.Page("pages/random_game.py", title="Guess the Number", icon=":material/casino:"),
        st.Page("pages/tic_tac_toe.py", title="Tic Tac Toe", icon=":material/games:"),
    ],
    " 👤 Account": [
        st.Page("pages/feedback.py", title="Feedback", icon=":material/feedback:"),
        st.Page("pages/contact_us.py", title="Contact Us", icon=":material/contact_mail:"),
        st.Page("pages/terms.py", title="Terms of Service", icon=":material/gavel:"),
    ],
    " 📚 Resources": [
        st.Page("pages/resource.py", title="Contents", icon=":material/library_books:"),
    ]
}

if st.session_state.get("role") in ["User"]:
    pg = st.navigation(pages)
elif st.session_state.get("role") in ["Responder"]:
    pg = st.navigation(pages1)
else:
    pg = st.navigation([st.Page("Home.py", title="Home", icon=":material/home:")])

pg.run()