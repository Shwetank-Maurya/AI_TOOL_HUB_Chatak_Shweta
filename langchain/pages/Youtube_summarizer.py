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
import time

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

st.title("Support by chatak Shweta")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Get the Best Summarizations from the Youtube Link</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Paste the Link and Hold the Cup , To roll out And Enjoy the Summary...
    </p>
</div>
""", unsafe_allow_html=True)

video_url = st.text_input(
    label='Paste the YouTube Link',
    placeholder='e.g. https://www.youtube.com/watch?v=Ks-_Mh1QhMc'
)


if video_url:
    with st.spinner("Working on the Video"):
        video_id=(video_url.split('='))
        video_id=video_id[-1]
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript(['de', 'en','hi'])
            transcript_data = transcript.fetch()
        
            transcript_text = " ".join([t.text for t in transcript_data])
            
            # st.write(transcript_text)
        
        except TranscriptsDisabled:
            print("No captions available for this video.")
        # st.write(transcript_text)
        load_dotenv()
        API=st.secrets["api"]["GROQ_API_KEY"]
        model=ChatGroq(api_key=API,model="llama-3.3-70b-versatile")
        prompt=PromptTemplate(
            template="""
            You are a Smart Youtube Video Summarizer assistant.
            summarize ONLY from the provided transcript context.
            And reply in a person like module,keeping the facts and original context.
            If the context is insufficient,just say Not Getting the Clear transcript or Language Not Detected.
        
            {context}
            """,
            input_variables=['context']
        )
        # st.write(context_text)
        final_prompt=prompt.invoke({'context':transcript_text})
            # st.write(final_prompt)
        answer=model.invoke(final_prompt)
        st.write(answer.content)
        st.toast("Summarized the Video!!!",icon='👍')
        time.sleep(0.5)


        