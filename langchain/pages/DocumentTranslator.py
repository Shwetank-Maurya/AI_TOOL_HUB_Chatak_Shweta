from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv
import time
import streamlit_extras.badges as badge
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
st.title("Translate Your Docs:")
load_dotenv()
API = st.secrets["api"]["GROQ_API_KEY"]
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>High Quality Translations</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Select the Source Language and Target Language And Upload the Docs.
    </p>
</div>
""", unsafe_allow_html=True)

languages = [
    'English', 'Hindi', 'Japanese', 'Chinese', 'Spanish', 'French', 'Arabic',
    'Russian', 'German', 'Portuguese', 'Italian', 'Korean', 'Dutch', 'Turkish',
    'Polish', 'Thai', 'Vietnamese', 'Indonesian', 'Hebrew', 'Greek', 'Swedish',
    'Danish', 'Finnish', 'Norwegian', 'Romanian', 'Hungarian', 'Czech', 'Ukrainian',
    'Bengali', 'Tamil', 'Telugu', 'Urdu', 'Persian', 'Malay', 'Swahili', 'Filipino'
]
rows=st.columns(2)
with rows[0]:
    src_language = st.selectbox("Source Language", options=languages)
with rows[1]:
    trg_language = st.selectbox("Target Language", options=languages)
user_input = st.text_area("Enter the text")

if st.button("Get Translation") and user_input:
    with st.spinner("Getting Translations..."):
        try:
            prompt = PromptTemplate(
                template="""
                As a professional translator, strictly follow these rules:
                1. Translate this {text} from {src} to {trg}
                2. Preserve technical terms (don't translate names/IDs)
                3. Maintain original formatting (line breaks/lists/tables)
                4. If languages are identical, return original text
                5. For untranslatable text, say: "[UNTRANSLATABLE CONTENT]"

                Translation:
                """,
                input_variables=['text', 'src', 'trg']
            )

            llm = ChatGroq(
                api_key=API,
                model="llama3-70b-8192",
                temperature=0.1  
            )

            final_prompt = prompt.invoke({
                'text': user_input,
                'src': src_language,
                'trg': trg_language
            })
            
            answer = llm.invoke(final_prompt)
            st.text_area("Translated text:", answer.content, height=300)
            st.toast("✅ Translation Complete")
            time.sleep(0.5)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Solutions:\n1. Check GROQ_API_KEY\n2. Try shorter text\n3. Retry in 1 min")