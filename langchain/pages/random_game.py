import streamlit as st
import random
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
st.title("Number Guessing Game")



st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;margin-bottom:30px; border-left: 5px solid #4e73df;'>
    <h3 style='color: #2e3a59;' >Choose a number between 1 to 100</h3>
    <h4 style='color: #2e3a59; margin-top: 0;'>Winning Probability - 0.01 %</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
    Stress Buster Enjoy the Game,
            Write to me if You are the lucky one who wins in this 0.01 %
            Every thing'll be fine...
    </p>
</div>
""", unsafe_allow_html=True)
number = random.randint(1, 100)

guess = st.number_input("Enter your guess:", min_value=1, max_value=100)

if st.button("Check"):
    if guess < number:
        st.error("Too low! Try again.")
    elif guess > number:
        st.error("Too high! Try again.")
    else:
        st.success(f"Correct! The number was {number}")
        st.balloons()