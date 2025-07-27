import os
import re
import json
import streamlit as st
import validators
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import streamlit_extras.badges as badge

st.set_page_config(page_title="AI Flashcard Generator", page_icon="📚")


with st.sidebar:
    st.markdown("### Connect with me")
    col1, col2 = st.columns(2)
    with col1:
        try:
            badge.badge(type="github", name="shwetank-maurya")
        except:
            st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Shwetank-blue?logo=github)](https://github.com/shwetank-maurya)")
    with col2:
        try:
            badge.badge(type="medium", name="shwetank_maurya")
        except:
            st.markdown("[![Medium](https://img.shields.io/badge/Medium-shwetank-blue?logo=medium)](https://medium.com/@shwetank_maurya)")


load_dotenv()
GROQ_API_KEY = st.secrets.get("api", {}).get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
if not GROQ_API_KEY:
    st.error("GROQ API key not found. Please configure it in secrets or environment variables.")
    st.stop()

llm = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivAPIWrapper()

st.title("📚 AI Flashcard Generator")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>One Stop Card Generator</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Convert any content into flashcards...
    </p>
</div>
""", unsafe_allow_html=True)

source = st.radio("Select content source:", 
                  ["Wikipedia", "Website URL", "arXiv Papers", "Custom Text"],
                  index=3,
                  horizontal=True)

content = ""
if source == "Wikipedia":
    query = st.text_input("Enter Wikipedia search term:")
    if query:
        with st.spinner("Fetching from Wikipedia..."):
            try:
                content = wikipedia.run(query)
                if content:
                    st.markdown("**Content Preview**")
                    st.write(content[:200] + "..." if len(content) > 200 else content)
                else:
                    st.warning("No content retrieved from Wikipedia. Try a different query.")
            except Exception as e:
                st.error(f"Failed to fetch Wikipedia content: {str(e)}")

elif source == "Website URL":
    url = st.text_input("Enter webpage URL:")
    if url:
        if not validators.url(url):
            st.error("Invalid URL. Please enter a valid HTTP/HTTPS URL.")
        else:
            with st.spinner("Scraping webpage..."):
                try:
                    loader = WebBaseLoader(url)
                    docs = loader.load()
                    content = docs[0].page_content
                    st.markdown("**Content Preview**")
                    st.write(content[:200] + "..." if len(content) > 200 else content)
                except Exception as e:
                    st.error(f"Failed to load webpage: {str(e)}")

elif source == "arXiv Papers":
    query = st.text_input("Enter arXiv search query:")
    if query:
        with st.spinner("Searching arXiv..."):
            try:
                content = arxiv.run(query)
                if content:
                    st.markdown("**Content Preview**")
                    st.write(content[:200] + "..." if len(content) > 200 else content)
                else:
                    st.warning("No content retrieved from arXiv. Try a different query.")
            except Exception as e:
                st.error(f"Failed to fetch arXiv content: {str(e)}")

else:
    content = st.text_area("Paste your content here:", height=200)

rowa = st.columns(2)
with rowa[0]:
    number = st.number_input("Number of Flashcards",
                             placeholder="Type a Number",
                             min_value=1,
                             max_value=50,
                             step=1,
                             value=5)
with rowa[1]:
    type = st.selectbox("Choose the Type",
                        options=['Fill in the Blanks', 'True/False', 'Question/Answer'],
                        index=None,
                        placeholder="Select a type")

Generate = st.button("Generate", disabled=not (content.strip() and number and type))

prompt = PromptTemplate(
    template="""
    You are a Flashcard Generator Assistant. Generate {number} flashcards based on the provided {context}. 
    The flashcards must be of the type '{type}' (e.g., 'Fill in the Blanks', 'True/False', or 'Question/Answer'). 
    For each flashcard, provide a clear question and answer pair, separated by a line. 
    Format the output as a numbered list, with each flashcard separated by a blank line.
    
    Context: {context}
    Number of Flashcards: {number}
    Type: {type}
    """,
    input_variables=['context', 'number', 'type']
)

if content and number and type and Generate:
    if len(content) > 3000:
        content = content[:3000] + "... [Content truncated]"
        st.warning("Content was truncated to fit token limits.")
    
    if not content.strip():
        st.error("No valid content provided. Please check your input or try a different source.")
        st.stop()

    final_prompt = prompt.invoke({'context': content, 'number': number, 'type': type})
    try:
        with st.spinner("Generating flashcards..."):
            answer = llm.invoke(final_prompt)
            if answer and answer.content.strip():
                with st.container(border=True):
                    st.markdown("**Generated Flashcards**")
                    flashcards = answer.content.split("\n\n")
                    for i, card in enumerate(flashcards, 1):
                        st.markdown(f"**Flashcard {i}**")
                        st.write(card)
                    json_data = json.dumps({"flashcards": [card.strip() for card in flashcards if card.strip()]}, indent=2)
                    st.download_button(
                        label="Download Flashcards as JSON",
                        data=json_data,
                        file_name="flashcards.json",
                        mime="application/json"
                    )
            else:
                st.error("No flashcards generated. Try adjusting the input or number of cards.")
    except Exception as e:
        st.error(f"Error generating flashcards: {str(e)}")
