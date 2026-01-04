import streamlit as st
import uuid

from core.arslm_engine import arslm_generate
from core.template_engine import list_templates, load_template, render_template
from core.memory_engine import append_message, get_history

st.set_page_config(page_title="MicroLLM No-Code", layout="wide")

st.title("🧠 MicroLLM No-Code")
st.caption("Powered by ARSLM")

session_id = st.session_state.setdefault("session_id", str(uuid.uuid4()))

template_name = st.selectbox("Template", list_templates())
template_text = load_template(template_name)

user_input = st.text_area("Your input")

if st.button("🚀 Generate"):
    history = get_history(session_id)
    prompt = render_template(template_text, user_input, history)

    append_message(session_id, "user", user_input)
    response = arslm_generate(prompt)
    append_message(session_id, "assistant", response)

    st.markdown("### 🤖 Response")
    st.markdown(response)