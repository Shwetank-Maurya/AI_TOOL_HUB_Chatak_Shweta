import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import streamlit_extras.badges as badge
from dotenv import load_dotenv
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

load_dotenv()
GROQ_API_KEY = st.secrets["api"]["GROQ_API_KEY"]

st.title("Grammar Checker")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>No Errors</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Getting Errors, Now No Problem Debug with this Tools...
    </p>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area("Enter the text", height=300)

if st.button("Debug"):
    
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Checking..."):

            
            prompt_template = PromptTemplate(
                input_variables=["user_text"],
                template="""
Act as a strict but helpful English teacher. Follow these steps:

1. **Corrected Version**: Provide a grammatically perfect version of the user's text: "{user_text}"
2. **Error Breakdown**: List each error in this format:
   - **Error type**: (e.g., subject-verb agreement, tense misuse)
   - **Incorrect**: [quote the problematic phrase]
   - **Correct**: [show fixed version]
   - **Rule**: Explain the grammar rule in simple terms (1-2 sentences).
3. **Improvement Suggestions**: Offer 1-2 alternative phrasings (if applicable) to enhance clarity/style.
4. **Tone Preservation**: Ensure the corrected text maintains the original tone (formal/casual).

Example Output:
(Your structured answer here)
"""

            )

            
            formatted_prompt = prompt_template.invoke({'user_text':user_input})

            
            llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192")
            response = llm.invoke(formatted_prompt)

            
            st.subheader("Correction and Feedback:")
            st.text_area("Output", response.content, height=300)
