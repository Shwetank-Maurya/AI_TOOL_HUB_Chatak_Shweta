import streamlit as st
import pandas as pd

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
st.title(" Contact Information")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df; margin-bottom: 30px;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Contact Us</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
        Try the Feedbacks...
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])  

with col1:
    with st.container():
        st.write("The Name is Master Shwetank Maurya")
        st.write("Location: Khelgaon Housing Complex, Hotwar, Ranchi, Jharkhand, India")
        st.write("Phone: +91 99999 00000")
        st.write("Email: sd3564086@gmail.com")
        st.write("Work Email: 404.found.bot@gmail.com")


with col2:
    with st.container(border=True):
        map_data = pd.DataFrame({
            "lat": [23.390967066429578],
            "lon": [85.39205011425607]
        })
        st.map(map_data, zoom=14, use_container_width=True)

