
import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="AFL Assistant", page_icon="🏉", layout="centered")
st.title("🏉 AFL Assistant")
st.caption("Factual Q&A · Stats retrieval · Match/player predictions — powered by LangGraph + Groq")

if "history" not in st.session_state:
    st.session_state.history = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

with st.sidebar:
    st.header("Session")
    if st.button("New conversation"):
        st.session_state.history = []
        st.session_state.conversation_id = None
        st.rerun()
    st.write(f"Conversation: `{st.session_state.conversation_id or 'new'}`")
    st.divider()
    st.markdown("**Example queries:**")
    st.markdown("- Will the Pies beat the Cats this week?")
    st.markdown("- What were Collingwood's stats last round?")
    st.markdown("- Who will top-score for Richmond?")
    st.markdown("- What's the weather in Sydney? *(off-topic)*")

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

if prompt := st.chat_input("Ask about AFL..."):
    st.session_state.history.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(f"{API}/chat",
                                  json={"message": prompt,
                                        "conversation_id": st.session_state.conversation_id},
                                  timeout=60)
                data = r.json()
                st.session_state.conversation_id = data.get("conversation_id")
                response = data.get("response","")
                st.markdown(response)
                st.caption(f"intent: `{data['intent']}` · latency: `{data['latency_ms']}ms` · "
                           f"validation: `{data['validation']}`")
                st.session_state.history.append({"role":"assistant","content":response})
            except Exception as e:
                st.error(f"API error: {e}")
