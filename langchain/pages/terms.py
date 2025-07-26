
import streamlit as st
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
            badge(type="medium", name="shwetank-maurya")
        except:
            st.markdown("[![medium](https://img.shields.io/badge/Medium-shwetank-blue?logo=medium)](https://medium.com/@shwetank_maurya)")
def show_terms_page():
 
    st.set_page_config(
        page_title="Terms of Service | AI Tool Selector",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
   
    st.markdown("""
    <style>
        .terms-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .terms-header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .terms-section {
            margin-bottom: 2rem;
        }
        .terms-section h2 {
            color: #2980b9;
            font-size: 1.3rem;
            margin-top: 1.5rem;
        }
        .terms-section h3 {
            color: #16a085;
            font-size: 1.1rem;
            margin-top: 1rem;
        }
        .terms-list {
            padding-left: 1.5rem;
            margin: 0.5rem 0;
        }
        .terms-list li {
            margin-bottom: 0.5rem;
        }
        .accept-btn {
            background-color: #3498db !important;
            color: white !important;
            font-weight: bold !important;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
    with st.container():
        st.markdown('<div class="terms-container">', unsafe_allow_html=True)
        
        
        st.markdown('<h1 class="terms-header">Terms of Service</h1>', unsafe_allow_html=True)
        st.markdown('**Last Updated:** July 25, 2025')
        st.markdown('---')
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown("""
        Welcome to AI Tool Selector! These Terms of Service ("Terms") govern your use of our application 
        and services. Please read them carefully before using our platform.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>1. Acceptance of Terms</h2>', unsafe_allow_html=True)
        st.markdown("""
        By accessing or using AI Tool Selector, you agree to be bound by these Terms. If you do not agree 
        to all the Terms , Use the App , I'll not say something.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>2. Description of Service</h2>', unsafe_allow_html=True)
        st.markdown("""
        The App provides a platform for users to access AI-powered tools, including but not limited to 
        YouTube Q&A, PDF summarization, grammar checking, document translation, flashcard generation, 
        and interactive games. The App is offered free of charge with unlimited usage quotas.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>3. Eligibility</h2>', unsafe_allow_html=True)
        st.markdown("""
        You must be a Human to use the App. Because , I didn't made this for Animals or Aliens.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>4. User Conduct</h2>', unsafe_allow_html=True)
        st.markdown('<h3>You agree to use the App only for lawful purposes and in accordance with these Terms. You must not:</h3>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="terms-list">
            <li>Violate any applicable laws or regulations.</li>
            <li>Attempt to reverse-engineer, decompile, or extract the App’s source code.</li>
            <li>Use the App to harass, harm, or defame others.</li>
            <li>Upload or share content that is illegal, offensive, or infringing on intellectual property rights.</li>
            <li>Interfere with the App’s functionality or security.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>5. Intellectual Property</h2>', unsafe_allow_html=True)
        st.markdown("""
        The App and its original content, features, and functionality are owned by the developer and 
        protected by intellectual property laws. You retain ownership of any content you create or 
        upload (e.g., PDFs, text), if in case you do so , I'll be happy.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
       
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>6. Third-Party Links</h2>', unsafe_allow_html=True)
        st.markdown("""
        The App may contain links to external sites (e.g., GitHub, Medium profiles,JotForms). These are provided 
        for convenience, and the developer is not responsible for the content or practices of these 
        third-party sites , 'cause they have their own terms of Service How can I be responsible , If You have any spare time
        Go and checkout those , But After reading mine one.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>7. Limitation of Liability</h2>', unsafe_allow_html=True)
        st.markdown("""
        The App is provided "as is" with warranties of somekind If You are reading this I owe you an ice-cream. But, I 
        am not liable for any indirect, incidental, or consequential damages arising from 
        your use of the App.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
       
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>8. Termination</h2>', unsafe_allow_html=True)
        st.markdown("""
        Yes,Here is my Power- I reserves the right to suspend or terminate your access to the App at any time, 
        with or without notice, if you violate these Terms or for operational reasons. Upon 
        termination, your right to use the App ceases immediately. And You donot Have any claim over this.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>9. Changes to Terms</h2>', unsafe_allow_html=True)
        st.markdown("""
        These Terms may be updated periodically. Continued use of the App after changes are posted 
        constitutes your acceptance of the new Terms. Check this document regularly for updates . But Don't worry
        I'll update you whenever I gonna update those.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>10. Governing Law</h2>', unsafe_allow_html=True)
        st.markdown("""
        These Terms are governed by the laws of India. Any disputes will be resolved in the hostels
        of IIIT Ranchi 'Block-4 603-C' . And , Yes If you are coming bring me something from the "Medha".
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="terms-section">', unsafe_allow_html=True)
        st.markdown('<h2>11. Contact Information</h2>', unsafe_allow_html=True)
        st.markdown("""
        For questions about these Terms, please contact us at:
        <br><br>
        <strong>Email:</strong> sd3564086@gmail.com<br>
        <strong>Email:</strong> 404.found.bot@gmail.com<br>
        <strong>Address:</strong> Ranchi , India , Asia , Earth , Universe
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        if st.button("I Accept These Terms", key="accept_terms", help="By clicking this button you acknowledge reading our Terms"):
            st.session_state.terms_accepted = True
            st.success("Thank you for accepting our Terms of Service!")
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True) 


if __name__ == "__main__":
    show_terms_page()