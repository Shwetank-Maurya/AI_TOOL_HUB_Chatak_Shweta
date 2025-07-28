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
            badge(type="medium", name="shwetank-maurya")
        except:
            st.markdown("[![medium](https://img.shields.io/badge/Medium-shwetank-blue?logo=medium)](https://medium.com/@shwetank_maurya)")


st.title("Support by chatak Shweta")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Get the Best Summarizations from the Youtube Link</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Paste the Link and Hold the Cup, To roll out And Enjoy the Summary...
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

def get_transcript_with_retries(video_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
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

def get_summary(transcript_text, api_key):
    try:
        model = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile")
        
        prompt = PromptTemplate(
            template="""
            You are an expert YouTube Video Summarizer assistant.
            
            Please provide a comprehensive summary of the video based on the transcript below.
            Structure your response as follows:
            
            ## 📋 Video Summary
            
            ### 🎯 Main Topic
            [Brief description of what the video is about]
            
            ### 🔑 Key Points
            [List the main points discussed in the video]
            
            ### 💡 Key Insights/Takeaways
            [Important insights or conclusions from the video]
            
            ### ⏱️ Duration Context
            [Brief mention of video length/pacing if relevant]
            
            ---
            
            **Instructions:**
            - Summarize ONLY from the provided transcript context
            - Write in a conversational, engaging tone
            - Keep the facts and original context intact
            - If the transcript is unclear or insufficient, mention it
            - Focus on the most important and actionable information
            
            **Transcript:**
            {context}
            """,
            input_variables=['context']
        )
        
        final_prompt = prompt.invoke({'context': transcript_text})
        response = model.invoke(final_prompt)
        return response.content, None
        
    except Exception as e:
        return None, f"Error generating summary: {str(e)}"

if 'transcript_cache' not in st.session_state:
    st.session_state.transcript_cache = {}

video_url = st.text_input(
    label='Paste the YouTube Link',
    placeholder='e.g. https://www.youtube.com/watch?v=Ks-_Mh1QhMc',
    help="Supports various YouTube URL formats including youtu.be links"
)

if video_url:
    video_id = extract_video_id(video_url)
    
    st.info(f"**Video ID:** {video_id}")
    
    try:
        st.video(f"https://www.youtube.com/watch?v={video_id}")
    except:
        pass
    
    if st.button("🔍 Generate Summary", type="primary"):
        cache_key = video_id
        if cache_key in st.session_state.transcript_cache:
            transcript_text, summary = st.session_state.transcript_cache[cache_key]
            st.success("📋 Using cached transcript")
        else:
            with st.spinner("🎥 Fetching video transcript..."):
                transcript_data, error = get_transcript_with_retries(video_id)
                
                if error:
                    st.error(f"❌ **Error:** {error}")
                    
                    with st.expander("🔧 Troubleshooting Tips"):
                        st.markdown("""
                        **Common solutions:**
                        
                        1. **Wait and retry** - YouTube may be temporarily blocking requests
                        2. **Check video settings** - Ensure the video is public and has captions
                        3. **Try a different video** - Some videos have restricted transcript access
                        4. **Verify URL format** - Make sure you're using a valid YouTube URL
                        
                        **Supported URL formats:**
                        - `https://www.youtube.com/watch?v=VIDEO_ID`
                        - `https://youtu.be/VIDEO_ID`
                        - `https://www.youtube.com/embed/VIDEO_ID`
                        """)
                    st.stop()
                
                transcript_text = clean_transcript_text(transcript_data)
                
                if not transcript_text:
                    st.error("❌ **Error:** Empty transcript received")
                    st.stop()
            
            with st.spinner("🤖 Generating AI summary..."):
                load_dotenv()
                try:
                    api_key = st.secrets["api"]["GROQ_API_KEY"]
                except:
                    api_key = os.getenv("GROQ_API_KEY")
                    if not api_key:
                        st.error("❌ **Error:** GROQ_API_KEY not found in secrets or environment")
                        st.stop()
                
                summary, error = get_summary(transcript_text, api_key)
                
                if error:
                    st.error(f"❌ **Error generating summary:** {error}")
                    st.stop()
                
                st.session_state.transcript_cache[cache_key] = (transcript_text, summary)
        
        st.success("✅ **Summary Generated Successfully!**")
        
        st.markdown("---")
        st.markdown(summary)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Show Full Transcript"):
                with st.expander("📄 Full Video Transcript"):
                    st.text_area("Transcript", transcript_text, height=300)
        
        with col2:
            st.download_button(
                label="💾 Download Summary",
                data=summary,
                file_name=f"youtube_summary_{video_id}.txt",
                mime="text/plain"
            )
        
        with col3:
            st.download_button(
                label="📜 Download Transcript",
                data=transcript_text,
                file_name=f"youtube_transcript_{video_id}.txt",
                mime="text/plain"
            )
        
        st.toast("🎉 Video summarized successfully!", icon='✅')

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; font-size: 14px;'>
    Made with Sasta Love by Chatak Shweta
</div>
""", unsafe_allow_html=True)
