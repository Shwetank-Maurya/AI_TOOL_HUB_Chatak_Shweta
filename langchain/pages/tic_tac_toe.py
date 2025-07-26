import streamlit as st
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
st.title("Tic-Tac-Toe")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4e73df;'>
    <h4 style='color: #2e3a59; margin-top: 0;'>Tic=TAC=Toe!</h4>
    <p style='color: #6c757d; margin-bottom: 0;'>
    Stress Buster Enjoy the Game,
            Every thing'll be fine...
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
    st.session_state.current_player = 'X'

def handle_click(i):
    if st.session_state.board[i] == '':
        st.session_state.board[i] = st.session_state.current_player
        st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if st.button(st.session_state.board[i] if st.session_state.board[i] else ' ', 
                     key=f"btn_{i}", 
                     on_click=handle_click, 
                     args=(i,)):
            pass


winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  
    [0, 4, 8], [2, 4, 6]              
]

for combo in winning_combinations:
    a, b, c = combo
    if st.session_state.board[a] and st.session_state.board[a] == st.session_state.board[b] == st.session_state.board[c]:
        st.success(f"Player {st.session_state.board[a]} wins!")
        st.balloons()
        break

if st.button("Reset Game"):
    st.session_state.board = [''] * 9
    st.session_state.current_player = 'X'
    st.rerun()