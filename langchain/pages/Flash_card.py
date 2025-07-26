import os
import re
import json
import streamlit as st
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


llm = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivAPIWrapper()


st.title("📚 AI Flashcard Generator")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>One Stop Card Generator</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Convert any Content Into FlashCards...
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
            content = wikipedia.run(query)
            if content:
                st.text(f"Retrieved Wikipedia content about {query}")

elif source == "Website URL":
    url = st.text_input("Enter webpage URL:")
    if url:
        with st.spinner("Scraping webpage..."):
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                content = docs[0].page_content
                st.text(f"Loaded {len(content)} characters from webpage")
            except Exception as e:
                st.text(f"Failed to load webpage: {str(e)}")

elif source == "arXiv Papers":
    query = st.text_input("Enter arXiv search query:")
    if query:
        with st.spinner("Searching arXiv..."):
            content = arxiv.run(query)
            if content:
                st.text("Retrieved arXiv paper content")

else:
    content = st.text_input("Paste your content here:")

rowa=st.columns(2)
with rowa[0]:
    number=st.number_input("Number of Flash Cards",
                            placeholder="Type a Number",
                            min_value=0,
                            step=1,
                            value=0)
    
with rowa[1]:
    type=st.selectbox("Choose the Type",
                        options=['Fill in the Blanks','True/False','Question/Answer']
                        ,index=None)
Generate=st.button("Generate")
    
prompt=PromptTemplate(
        template="""
        You are a flash card Generator Assistant  , who genrates good question and answer based cards from the given {context}
        and You have to generate this much flash cards {number} and you have to follow what user says like true false means generate a true false based,and fill in the blanks means
        {type}You have to follow what user says,Seprate a single question and answer by a line give it in a way like a notebook

        {context}
        number:{number}
        type: {type}
        """,
        input_variables=['context','number','type']
)

if content and number and type and Generate:
    final_prompt=prompt.invoke({'context':content,'number':number,'type':type})
    answer=llm.invoke(final_prompt)
    if answer:
        with st.container(border=True):
            st.write(answer.content)
        


