import streamlit as st
import streamlit_extras.badges as badge
import time


st.set_page_config(
    page_title="AI Tools Selector",
    layout="wide",
    initial_sidebar_state='expanded'
)

with st.sidebar:
    st.markdown("### Connect with me")
    col1, col2 = st.columns(2)
    with col1:
        try:
            badge(type="github", name="shwetank-maurya")
        except:
            st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Shwetank-blue?logo=github)](https://github.com/shwetank-maurya)")
    with col2:
        try:
            badge(type="medium", name="shwetank_maurya")
        except:
            st.markdown("[![medium](https://img.shields.io/badge/Medium-shwetank-blue?logo=medium)](https://medium.com/@shwetank_maurya)")


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "User", "Responder", "Admin"]

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES, key="role_select")
    check = st.checkbox("I have read the Terms and Conditions and I do not have any claim over the Admin.")
    if st.button("Terms of Service"):
        with st.container(height=300):
            
                st.markdown("""
                ### Terms of Service
                **Last Updated:** July 25, 2025

                ---

                #### Welcome
                Welcome to AI Tool Selector! These Terms of Service ("Terms") explain how you can use our app and services. Please read them carefully before using our platform.

                #### 1. Acceptance of Terms
                By accessing or using AI Tool Selector, you agree to be bound by these Terms. If you do not agree 
                to all the Terms , Use the App , I'll not gonna say something

                #### 2. Description of Service
                The App provides a platform for users to access AI-powered tools, including but not limited to 
                YouTube Q&A, PDF summarization, grammar checking, document translation, flashcard generation, 
                and interactive games. The App is offered free of charge with unlimited usage quotas.
                #### 3. Eligibility
                You must be a Human to use the WebApp. Because , I didn't made this for Animals or Aliens.
                #### 4. User Conduct
                Use the app only for legal purposes and follow these Terms. You must not:
                - Break any laws or regulations.
                - Try to reverse-engineer or copy the app’s code.
                - Harass, harm, or defame others.
                - Upload illegal, offensive, or copyrighted content.
                - Disrupt the app’s functionality or security.

                #### 5. Intellectual Property
                The App and its original content, features, and functionality are owned by the developer and 
                protected by intellectual property laws. You retain ownership of any content you create or 
                upload (e.g., PDFs, text), if in case you do so , It'll make me happy.
                #### 6. Third-Party Links
                The App may contain links to external sites (e.g., GitHub, Medium profiles,JotForms). These are provided 
                for convenience, and the developer is not responsible for the content or practices of these 
                third-party sites , 'cause they have their own terms of Service How can I be responsible , If You have any spare time
                Go and checkout those , But After reading mine one.
                #### 7. Limitation of Liability
               The App is provided "as is" with warranties of somekind If You are reading this I owe you an ice-cream. But, I 
                am not liable for any indirect, incidental, or consequential damages arising from 
                your use of the App.
                #### 8. Termination
                Yes,Here is my Power- I reserves the right to suspend or terminate your access to the App at any time, 
                with or without notice, if you violate these Terms or for operational reasons. Upon 
                termination, your right to use the App ceases immediately. And You donot Have any claim over this

                #### 9. Changes to Terms
                These Terms may be updated periodically. Continued use of the App after changes are posted 
                constitutes your acceptance of the new Terms. Check this document regularly for updates . But Don't worry
                I'll update you whenever I gonna update those.

                #### 10. Governing Law
                These Terms are governed by the laws of India. Any disputes will be resolved in the hostels
                of IIIT Ranchi 'Block-4 603-C' . And , Yes If you are coming bring me something from the "Medha".

                #### 11. Contact Information
                For questions about these Terms, contact us at:
                - **Email:** sd3564086@gmail.com
                - **Email:** 404.found.bot@gmail.com
                - **Address:** Ranchi ,India 
                """)
            
    if role == "Admin":
        enable = st.checkbox("Verify Yourself")
        if enable:
            picture = st.camera_input("Verify", help="To Ensure The Admin")
            if picture:
                st.image(picture)
                st.error("Face Not Match, Invalid Credentials")
                st.toast("Invalid Authentication!!!")
                time.sleep(1)
                st.session_state.role = None  
                st.rerun()
    
    if st.button("Log in") and check:
        if role in ["User", "Responder"]:  
            st.session_state.role = role
        elif role == "Admin":
            st.session_state.role = None 
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

def main_page():
    st.title("AI Tool Selector")
    st.markdown("## Discover AI-Powered Tools")
    
    role = st.session_state.role
    if not role:
        login()  
    else:
        st.success(f"Logged in as: {st.session_state.role}")
        if st.session_state.role == "Admin":
            st.warning("Admin access is restricted. Please log in as User or Responder.")
        else:  
            ro = st.columns(2)
            with ro[0]:
                with st.container(height=400, border=False):
                    st.markdown("""
                    <div style="padding: 20px;">
                        <h3 style="color: #2c3e50;">Why Choose Our AI Toolbox?</h3>
                        <ul style="font-size: 1.1rem;">
                            <li>🚀 All-in-one solution for your AI needs</li>
                            <li>⏱️ Save time with automated workflows</li>
                            <li>🔍 Advanced processing for YouTube, PDFs and more</li>
                            <li>🎮 Fun interactive games included</li>
                            <li>💯 Free to use with no hidden costs</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            
            with ro[1]:
                st.image("langchain/References/Home_Girl.gif")
            
            st.markdown("""
            <style>
                .tile-container {
                    border-radius: 15px;
                    padding: 10px;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(5px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: all 0.3s ease;
                    height: 300px;
                    margin-bottom: 20px;
                }
                .tile-container:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                }
                .tile-image {
                    width: 100%;
                    height: 180px;
                    object-fit: cover;
                    border-radius: 10px;
                }
                .stLinkButton {
                    width: 100%;
                    margin-top: 10px;
                    background: linear-gradient(45deg, #FF4B4B, #FF8E8E) !important;
                    color: white !important;
                    border: none !important;
                    font-weight: bold !important;
                }
                .stLinkButton:hover {
                    background: linear-gradient(45deg, #FF8E8E, #FF4B4B) !important;
                }
            </style>
            """, unsafe_allow_html=True)

            st.subheader("Core Features")
            row1 = st.columns(4)
            with row1[2].container():
                st.image("langchain/References/Youtube.png", use_container_width=True)
                if st.button("YouTube Q&A", help="Talk to our YouTube Based Algorithm", key="youtube_qa"):
                    st.switch_page("pages/main.py")
            with row1[1].container():
                st.image("langchain/References/ghre.jpg", use_container_width=True)
                if st.button("Document Translator", help="Translate documents between languages", key="doc_translator"):
                    st.switch_page("pages/DocumentTranslator.py")
            with row1[0].container():
                st.image("langchain/References/Ai.jpg", use_container_width=True)
                if st.button("AI Chat Bot", help="Conversational AI assistant", key="ai_chat"):
                    st.switch_page("pages/Bot.py")

            with row1[3].container():
                st.image("https://images.unsplash.com/photo-1649877508777-1554357604eb?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)
                if st.button("PDF Summarizer", help="Summarize your PDF documents", key="pdf_summarizer"):
                    st.switch_page("pages/pdf_summarizer.py")

            st.subheader("Productivity Tools")
            row2 = st.columns(4)
            with row2[0].container():
                st.image("langchain/References/Grammer.jpg", use_container_width=True)
                if st.button("Grammar Checker", help="Check and improve your writing", key="grammar_checker"):
                    st.switch_page("pages/grammer.py")
            with row2[1].container():
                st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhbnNsYXRpb258ZW58MHwyfDB8fHww", use_container_width=True)
                if st.button("PDF Q&A", help="Get answers from your PDF documents", key="pdf_qa"):
                    st.switch_page("pages/pdf_summarizer.py")
            with row2[2].container():
                st.image("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Zmxhc2hjYXJkc3xlbnwwfDJ8MHx8fDA%3D", use_container_width=True)
                if st.button("FlashCard Generator", help="Create study flashcards automatically", key="flashcards"):
                    st.switch_page("pages/Flash_card.py")
            with row2[3].container():
                st.image("langchain/References/YoutubeSma.jpg", use_container_width=True)
                if st.button("YouTube Summary", help="Get summaries of YouTube videos", key="youtube_summary"):
                    st.switch_page("pages/Youtube_summarizer.py")

            st.subheader("Fun Zone")
            row3 = st.columns(4)
            with row3[1].container():
                st.image("langchain/References/Game@.png", use_container_width=True)
                if st.button("Guess the Number", help="Try to guess the secret number", key="guess_number"):
                    st.switch_page("pages/random_game.py")

            with row3[2].container():
                st.image("langchain/References/TicTac_TOE.png", use_container_width=True)
                if st.button("Tic Tac Toe", help="Play the classic game", key="tic_tac_toe"):
                    st.switch_page("pages/tic_tac_toe.py")

            st.divider()
            
            footer = st.columns(3)
            with footer[0]:
                st.button("© 2025 AI Tools Hub")
            with footer[2]:
                if st.button("Log out"):
                    logout()
            st.markdown("---")


if __name__ == "__main__":
    main_page()