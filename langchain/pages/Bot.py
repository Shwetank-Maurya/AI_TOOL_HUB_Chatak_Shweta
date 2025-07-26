import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import streamlit_extras.badges as badge
import json
import tempfile
import atexit
import time
from datetime import datetime


load_dotenv()
API = st.secrets["api"]["GROQ_API_KEY"]
if not API:
    st.error("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()


modelbot = ChatGroq(api_key=API, model="llama-3.3-70b-versatile")

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

st.title("Chat with Chatak Shweta!!!")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Ask Anything to Me!</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
            Hello! I’m Chatak Shweta, your friendly AI assistant. How can I help you today?
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown(
    """
    <style>
    .chat-container {
        padding: 10px;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .message {
        margin: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        clear: both;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        float: right;
    }
    .assistant-message {
        background-color: #e9ecef;
        color: #333;
        float: left;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
temp_file_path = temp_file.name
temp_file.close()


if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        with open(temp_file_path, "r") as f:
            stored_messages = json.load(f)
            for msg in stored_messages:
                st.session_state.messages.append(HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]))
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.messages = []

messages = st.container()
for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    content = msg.content
    avatar_url = "https://images.unsplash.com/photo-1717501220725-83f151c447e7?w=40&h=40&fit=crop" if role == "assistant" else None
    if avatar_url:
        messages.markdown(
            f'<div class="message assistant-message"><img src="{avatar_url}" class="avatar"> {content}</div>',
            unsafe_allow_html=True,
        )
    else:
        messages.markdown(f'<div class="message user-message">{content}</div>', unsafe_allow_html=True)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are Chatak Shweta, a friendly AI assistant. Use the conversation history to provide context-aware responses."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}"),
    ]
)

if prompt_input := st.chat_input("Type your message..."):
  
    user_msg = HumanMessage(content=prompt_input)
    st.session_state.messages.append(user_msg)
    messages.markdown(f'<div class="message user-message">{prompt_input}</div>', unsafe_allow_html=True)

    time.sleep(1)  


    chat_history = st.session_state.messages[:-1]  
    response = modelbot.invoke(prompt.format_prompt(chat_history=chat_history, user_input=prompt_input).to_messages())
    assistant_msg = AIMessage(content=response.content)
    st.session_state.messages.append(assistant_msg)
    messages.markdown(
        f'<div class="message assistant-message"><img src="https://images.unsplash.com/photo-1717501220725-83f151c447e7?w=40&h=40&fit=crop" class="avatar"> {response.content}</div>',
        unsafe_allow_html=True,
    )

    with open(temp_file_path, "w") as f:
        json.dump([{"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content} for msg in st.session_state.messages], f)


if st.button("Clear Chat"):
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        st.success("Chat history cleared. Temp file and context deleted.")
        st.session_state.messages = []
        st.rerun()


@atexit.register
def cleanup():
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)