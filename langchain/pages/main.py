import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, 
    RequestBlocked, 
    VideoUnavailable,
    NoTranscriptFound
)
from dotenv import load_dotenv
import streamlit_extras.badges as badge
import time
import re

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

def extract_video_id(url):
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
        r'youtube\.com\/.*[?&]v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return url.strip()

def get_language_codes(language):
    language_map = {
        "English": ['en', 'en-US', 'en-GB'],
        "Hindi": ['hi'],
        "Tamil": ['ta'],
        "Telugu": ['te'],
        "Marathi": ['mr'],
    }
    return language_map.get(language, [language.lower()[:2]])

def get_transcript_with_retries(video_id, language_codes, max_retries=3):
    for attempt in range(max_retries):
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list_transcripts(video_id)
            
            try:
                transcript = transcript_list.find_transcript(language_codes)
            except NoTranscriptFound:
                try:
                    transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
                except NoTranscriptFound:
                    try:
                        transcript = transcript_list.find_transcript(['hi', 'de', 'es', 'fr'])
                    except NoTranscriptFound:
                        available_transcripts = list(transcript_list)
                        if available_transcripts:
                            transcript = available_transcripts[0]
                        else:
                            return None, "No transcripts available for this video"
            
            transcript_data = transcript.fetch()
            return transcript_data, None
            
        except RequestBlocked:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                st.warning(f"Request blocked, retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                return None, "Request blocked by YouTube. Please try again later or use a different video."
                
        except TranscriptsDisabled:
            return None, "Transcripts/captions are disabled for this video."
            
        except VideoUnavailable:
            return None, "Video is unavailable or private."
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error occurred: {str(e)}. Retrying...")
                time.sleep(2)
                continue
            else:
                return None, f"Error fetching transcript: {str(e)}"
    
    return None, "Failed to fetch transcript after multiple attempts."

def clean_transcript_text(transcript_data):
    if not transcript_data:
        return ""
    
    transcript_text = " ".join([t.get('text', '') for t in transcript_data])
    transcript_text = re.sub(r'\[.*?\]', '', transcript_text)
    transcript_text = re.sub(r'\s+', ' ', transcript_text)
    transcript_text = transcript_text.strip()
    
    return transcript_text

if 'qa_cache' not in st.session_state:
    st.session_state.qa_cache = {}

video_url = st.text_input(
    label='Paste the YouTube Link',
    placeholder='e.g. https://www.youtube.com/watch?v=Ks-_Mh1QhMc'
)

select_box = st.selectbox('What is the language of the Video?',                               
                         options=[
                             "English",
                             "Hindi", 
                             "Tamil",
                             "Telugu",
                             "Marathi",
                             "Any other"
                         ], index=None)

if select_box == "Any other":
    transcript_language = st.text_input("Enter the language of the Video:")
else:
    transcript_language = select_box

if video_url and select_box:
    video_id = extract_video_id(video_url)
    
    st.info(f"**Video ID:** {video_id}")
    
    try:
        st.video(f"https://www.youtube.com/watch?v={video_id}")
    except:
        pass
    
    cache_key = f"{video_id}_{transcript_language}"
    
    if cache_key not in st.session_state.qa_cache:
        with st.spinner("📥 Processing video transcript..."):
            language_codes = get_language_codes(transcript_language)
            
            transcript_data, error = get_transcript_with_retries(video_id, language_codes)
            
            if error:
                st.error(f"❌ **Error:** {error}")
                
                with st.expander("🔧 Troubleshooting Tips"):
                    st.markdown("""
                    **Common solutions:**
                    
                    1. **Wait and retry** - YouTube may be temporarily blocking requests
                    2. **Check video settings** - Ensure the video is public and has captions
                    3. **Try a different video** - Some videos have restricted transcript access
                    4. **Check language availability** - The selected language might not be available
                    5. **Try "English"** - Most videos have English captions
                    """)
                st.stop()
            
            transcript_text = clean_transcript_text(transcript_data)
            
            if not transcript_text:
                st.error("❌ **Error:** Empty transcript received")
                st.stop()
                
            try:
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.create_documents([transcript_text])
                
                load_dotenv()
                try:
                    API = st.secrets["api"]["GROQ_API_KEY"]
                    API3 = st.secrets["api"]["HUGGINGFACEHUB_API_TOKEN"]
                except:
                    API = os.getenv("GROQ_API_KEY")
                    API3 = os.getenv("HUGGINGFACEHUB_API_TOKEN")
                    if not API or not API3:
                        st.error("❌ **Error:** API keys not found in secrets or environment")
                        st.stop()
                
                model = ChatGroq(api_key=API, model="llama-3.3-70b-versatile")
                embeddings = HuggingFaceEndpointEmbeddings(
                    model="BAAI/bge-small-en-v1.5",  
                    huggingfacehub_api_token=API3  
                )
                
                vector_store = FAISS.from_documents(chunks, embeddings)
                retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={"k": 5})
                
                st.session_state.qa_cache[cache_key] = {
                    'retriever': retriever,
                    'model': model,
                    'transcript_text': transcript_text
                }
                
                st.success("✅ **Video processed successfully!** You can now ask questions.")
                
            except Exception as e:
                st.error(f"❌ **Error processing video:** {str(e)}")
                st.stop()
    else:
        st.success("📋 **Using cached video data.** You can ask questions below.")
    
    if cache_key in st.session_state.qa_cache:
        retriever = st.session_state.qa_cache[cache_key]['retriever']
        model = st.session_state.qa_cache[cache_key]['model']
        transcript_text = st.session_state.qa_cache[cache_key]['transcript_text']
        
        st.markdown("---")
        st.markdown("### 🤔 Ask Your Question")
        
        question = st.text_input(
            label='Describe the question of which you want the answer from the Content',
            placeholder="e.g. Is perceptron discussed in this Video?",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("🔍 Ask Question", type="primary")
        
        if question and ask_button:
            with st.spinner("🔍 Searching for answer..."):
                try:
                    retrieved_docs = retriever.invoke(question)
                    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
                    
                    prompt = PromptTemplate(
                        template="""
                        You are a helpful assistant specialized in answering questions about YouTube video content.
                        
                        **Instructions:**
                        - Answer ONLY from the provided transcript context below
                        - If the context doesn't contain enough information to answer the question, say "I don't have enough information from this video to answer that question."
                        - Be specific and cite relevant parts when possible
                        - Keep your answer concise but complete
                        - If you're unsure, it's better to say you don't know than to guess
                        
                        **Context from the video:**
                        {context}
                        
                        **Question:** {question}
                        
                        **Answer:**
                        """,
                        input_variables=['context', 'question']
                    )
                    
                    final_prompt = prompt.invoke({'context': context_text, 'question': question})
                    answer = model.invoke(final_prompt)
                    
                    st.markdown("### 💬 Answer")
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {answer.content}")
                    
                    with st.expander("📄 View Source Context"):
                        st.text_area("Relevant transcript sections:", context_text, height=200)
                    
                except Exception as e:
                    st.error(f"❌ **Error generating answer:** {str(e)}")
                    st.info("💡 **Tip:** Try rephrasing your question or try again after a moment.")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Show Full Transcript"):
                with st.expander("📄 Full Video Transcript"):
                    st.text_area("Complete Transcript", transcript_text, height=400)
        
        with col2:
            st.download_button(
                label="💾 Download Transcript",
                data=transcript_text,
                file_name=f"youtube_transcript_{video_id}.txt",
                mime="text/plain"
            )

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; font-size: 14px;'>
    Made with ❤️ by Chatak Shweta
</div>
""", unsafe_allow_html=True)
