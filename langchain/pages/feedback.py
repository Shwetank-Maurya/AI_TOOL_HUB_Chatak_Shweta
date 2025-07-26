import streamlit as st
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
st.title("Feedback")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Your Feedback Matters!</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
    Your feedback is incredibly valuable to us. It helps us grow, improve, 
    and implement the features you want to see.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  
st.markdown("""
<div style='text-align: center;'>
    <p style='color: #6c757d; margin-bottom: 8px; font-size: 14px;'>
    Share your suggestions and questions
    </p>
</div>
""", unsafe_allow_html=True)

st.link_button(
    "📝 Give Feedback", 
    'https://agent.jotform.com/01983dab2c8176d98229087264210c3f0492',
    help="Click to provide your valuable feedback",
    use_container_width=False
)