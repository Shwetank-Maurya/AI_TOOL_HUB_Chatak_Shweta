
import streamlit as st

pages = {
    "Home": [
        st.Page("Home.py", title="Home", icon="🏠")
    ],
    "Tools 1": [
        st.Page("pages/main.py", title="YouTube Q&A", icon="🎥"),
        st.Page("pages/Youtube_summarizer.py", title="YouTube Vid Summary", icon="📹"),
        st.Page("pages/Bot.py", title="Talk to Shweta", icon="🤖"),
        st.Page("pages/pdf_summarizer.py", title="PDF Support", icon="📑"),
    ],
    "Tools 2": [
        st.Page("pages/grammer.py", title="Grammer Checker", icon="✍️"),
        st.Page("pages/DocumentTranslator.py", title="Document Translator", icon="🌐"),
        st.Page("pages/Flash_card.py", title="FlashCard Generator", icon="📝"),
    ],
    "Fun Zone": [
        st.Page("pages/random_game.py", title="Guess the Number", icon="🎲"),
        st.Page("pages/tic_tac_toe.py", title="Tic Tac Toe", icon="🎮"),
    ],
    "Account": [
        st.Page("pages/feedback.py", title="Feedback", icon="💬"),
        st.Page("pages/contact_us.py", title="Contact Us", icon="📩"),
    ]
}

all_pages = []
for category, page_list in pages.items():
    all_pages.extend(page_list)

if st.session_state.get("role") in ["User", "Responder"]:
    
    pg = st.navigation(all_pages)
    
    
    with st.sidebar:
        st.title("Navigation")
        
        
        st.page_link("Home.py", label="Home", icon="🏠")
        st.divider()
        
        
        for category, page_list in pages.items():
            if category == "Home": 
                continue  
                
            with st.expander(f"{category}"):
                for page in page_list:
                    st.page_link(page, label=page.title, icon=page.icon)
        
        st.divider()
        
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            st.rerun()
            
else: 
    pg = st.navigation([st.Page("Home.py", title="Home", icon="🏠")])

pg.run()
