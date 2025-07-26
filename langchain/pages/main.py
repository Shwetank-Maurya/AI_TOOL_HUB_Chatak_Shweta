import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from dotenv import load_dotenv
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


st.title("Support by chatak Shweta")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>YouTube Video Q&A</h4>
    <h6 style='color: #2e3a59; margin-top: 0;'>Ask the questions from the Video</h6>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Stuck With the length , Don't Stop. Start with this , Paste the link and let the magic begin...
    </p>
</div>
""", unsafe_allow_html=True)


video_url = st.text_input(
    label='Paste the YouTube Link',
    placeholder='e.g. https://www.youtube.com/watch?v=Ks-_Mh1QhMc'
)
select_box=st.selectbox('What is the language of the Video?',                               
                                options=[
                                    "English",
                                    "Hindi",
                                    "Tamil",
                                    "Telgu",
                                    "Marathi",
                                    "Any other"
                                ],index=None)
if(select_box=="Any other"):
    transcript_language=st.text_input("Enter the language of the Video:")
else:
    transcript_language=select_box

if video_url and select_box :
    with st.spinner("In Progress..."):
        video_id=(video_url.split('='))
        video_id=video_id[-1]
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript(['de','hi','en'])
            transcript_data = transcript.fetch()
        
            transcript_text = " ".join([t.text for t in transcript_data])
            
            # st.write(transcript_text)
        
        except TranscriptsDisabled:
            print("No captions available for this video.")
        # st.write(transcript_text)
        splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        chunks=splitter.create_documents([transcript_text])
        # st.write(len(chunks))
        load_dotenv()
        API=st.secrets["api"]["GROQ_API_KEY"]
        model=ChatGroq(api_key=API,model="llama-3.3-70b-versatile")
        API3=st.secrets["api"]["HUGGINGFACEHUB_API_TOKEN"]
        embeddings = HuggingFaceEndpointEmbeddings(
        model="BAAI/bge-small-en-v1.5",  
        huggingfacehub_api_token=API3  
        )
        vector_store=FAISS.from_documents(chunks,embeddings)
        
        retriver=vector_store.as_retriever(search_type='similarity',search_kwargs={"k":5})
        if retriver:
            
                re=st.text_input(
                    label='Describe the question of which you want the answer from the Content',
                    placeholder="e.g. Is perceptron discussed in this Video?",
                    )
                

                prompt=PromptTemplate(
                    template="""
                    You are a helpful assistant.
                    Answer ONLY from the provided transcript context.
                    If the context is insufficient,just say you Don't Know.
                    And Also Include this line when you don't get the answer-
                    "Ask to Shweta,She Knows almost everything..."
                    
                    {context}
                    Question:{question}
                    """,
                    input_variables=['context','question']
                )
                with st.spinner("Just a sec..."):
                    retrieved_docs=retriver.invoke(re)
                    context_text="\n\n".join(doc.page_content for doc in retrieved_docs )
                    # st.write(context_text)
                    if re:
                        final_prompt=prompt.invoke({'context':context_text,'question':re})
                        # st.write(final_prompt)
                        answer=model.invoke(final_prompt)
                        st.write(answer.content)


        