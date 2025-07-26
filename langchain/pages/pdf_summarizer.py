import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
import tempfile
import os
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
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

if 'qa_processed' not in st.session_state:
    st.session_state.qa_processed = False
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None

st.title("PDF Summarizer and PDF Support")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Generate High Quality Summarization and Ask Questions with this Support!</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
    Upload the files (maximum size allowed is 200mb) and ask the queries...
    </p>
</div>
""", unsafe_allow_html=True)
load_dotenv()
API = st.secrets["api"]["GROQ_API_KEY"]
API2 = st.secrets["api"]["HUGGINGFACEHUB_API_TOKEN"]
model = ChatGroq(api_key=API, model="llama3-8b-8192")



st.divider()
uploaded_file = st.file_uploader("Upload the File", type="pdf")

if uploaded_file:
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        loader = PyMuPDFLoader(tmp_path)
        docs = loader.load()
        st.success(f"Successfully loaded {len(docs)} page(s)")
    except Exception as e:
        st.error("❌ Failed to load PDF")
        st.error(f"Error: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    left, middle, right = st.columns(3, vertical_alignment="bottom")
    clicked_summary = left.button("PDF Summary", help="Reach Here to get the PDF of the summary Generated.", icon=":material/picture_as_pdf:")
    clicked_qa = right.button("PDF Q&A", help="Want to Ask Something.", icon=":material/travel_explore:")

    if docs and clicked_summary:
        with st.spinner("Creating Summary..."):
            prompt = PromptTemplate(
                template="""You are an intelligent PDF summarization assistant.

                Your job is to:
                1. Summarize the given text clearly and concisely.
                2. Include relevant context from the provided documents to ensure the summary is accurate and informative.
                3. If the text is unclear, messy, or lacks sufficient context to summarize properly, respond with:
                **"⚠️ The text or context is unclear. Please provide a more complete or cleaner document."**

                Here is the context you need to use:
                {context}""",
                input_variables=['context']
            )
            
            context_text = "\n\n".join(doc.page_content for doc in docs)
            final_prompt = prompt.invoke({'context': context_text})
            answer = model.invoke(final_prompt)
            st.text_area("Summary of the context", answer.content, height=500)

    if docs and clicked_qa:
        st.session_state.qa_processed = True
        with st.spinner("Preparing Q&A system..."):
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents([doc.page_content for doc in docs])
            
            embeddings = HuggingFaceEndpointEmbeddings(
                model="BAAI/bge-small-en-v1.5",
                huggingfacehub_api_token=API2,
            )
            st.session_state.vector_store = FAISS.from_documents(chunks, embeddings)

if st.session_state.qa_processed and st.session_state.vector_store:
    retriever = st.session_state.vector_store.as_retriever(search_type='similarity', search_kwargs={"k":4})
    ques = st.text_input(
        label="What is the Question/topic from the PDF?",
        placeholder="e.g. Assumptions of the Linear Regression.",
        key="question_input"  
    )

    if ques:
        with st.spinner("Searching for answers..."):
            retrieved_docs_qA = retriever.invoke(ques)
            context_text_qA = "\n\n".join(doc.page_content for doc in retrieved_docs_qA)
            
            prompt_qA = PromptTemplate(
                template="""You are a helpful assistant.
                Answer ONLY from the provided context.
                If the context is insufficient, just say you Don't Know.
                And Also Include this line when you don't get the answer-
                "Ask to Shweta, She Knows almost everything..."
                
                {context}
                Question: {question}""",
                input_variables=['context', 'question']
            )
            
            final_qA_prompt = prompt_qA.invoke({
                'context': context_text_qA,
                'question': ques
            })
            
            answer_qA = model.invoke(final_qA_prompt)
            st.write("### Answer:")
            st.write(answer_qA.content)
