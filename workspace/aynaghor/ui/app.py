
import streamlit as st
from core.engine import Engine

st.title('AYNAGH0R – Dark & Erotic AI')

prompt = st.text_area('Your prompt')
if st.button('Generate'):
    eng = Engine()
    resp = eng.route(prompt)
    st.write(resp)
