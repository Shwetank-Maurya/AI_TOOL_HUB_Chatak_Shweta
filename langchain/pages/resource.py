import streamlit as st
from streamlit_extras.badges import badge 

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

st.title("Resources")

st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Contents</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        The Contents required for making this project...
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("### Useful Resources")

st.markdown("""
- **CampusX**: [YouTube Channel](https://www.youtube.com/c/CampusX-official)
- **LangChain Docs**: [Documentation](https://python.langchain.com/docs/get_started/introduction)
- **Streamlit Docs**: [Official Documentation](https://docs.streamlit.io/)
- **Streamlit Extras**: [Components Library](https://extras.streamlit.app/)
""")

