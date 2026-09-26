import streamlit as st

# ── ffmpeg fix — hardcoded, session/order se independent ──
from static_ffmpeg import run
_ffmpeg_path, _ = run.get_or_fetch_platform_executables_else_raise()
import os
os.environ["PATH"] = os.path.dirname(_ffmpeg_path) + os.pathsep + os.environ["PATH"]

import whisper, tempfile
from agent_core import run_agent, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

@st.cache_resource
def load_whisper():
    return whisper.load_model("small")

whisper_model = load_whisper()
END_PHRASES = ["bye", "allah hafiz", "khuda hafiz", "shukriya bye", "band karo", "call khatam"]

st.set_page_config(page_title="RealEstate Hub — Live Call", page_icon="\U0001F4DE")
st.title("\U0001F4DE RealEstate Hub — Live Call Demo")

if "call_active" not in st.session_state:
    st.session_state.call_active = False
if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns(2)
with col1:
    if st.button("\U0001F4DE Start Call", disabled=st.session_state.call_active):
        st.session_state.call_active = True
        st.session_state.history = []
        st.rerun()
with col2:
    if st.button("\U0001F534 End Call", disabled=not st.session_state.call_active):
        st.session_state.call_active = False
        st.rerun()

st.divider()

if st.session_state.call_active:
    st.success("Call in progress — bolo mic mein.")
    from audio_recorder_streamlit import audio_recorder
    audio_bytes = audio_recorder(text="Bolo", icon_size="2x", key="recorder")

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        with st.spinner("Sun raha hoon..."):
            result = whisper_model.transcribe(tmp_path, language="en")
            user_text = result["text"].strip()
        os.remove(tmp_path)
        st.chat_message("user").write(user_text)

        if any(p in user_text.lower() for p in END_PHRASES):
            reply_text = "Bohot shukriya, Allah Hafiz!"
            st.chat_message("assistant").write(reply_text)
            st.session_state.history.append({"user": user_text, "agent": "[Call ended]"})
            st.session_state.call_active = False
            st.rerun()
        else:
            with st.spinner("Ji, ek second sir..."):
                agent_result = run_agent(user_text, user_phone="0300-DEMO-CALL")
                reply_text = agent_result.get("response", "")
            st.chat_message("assistant").write(reply_text)
            st.session_state.history.append({"user": user_text, "agent": reply_text})

        if ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID:
            try:
                from elevenlabs.client import ElevenLabs
                import base64 as b64
                tts_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                audio = tts_client.text_to_speech.convert(
                    voice_id=ELEVENLABS_VOICE_ID, text=reply_text, model_id="eleven_multilingual_v2")
                b64_audio = b64.b64encode(b"".join(audio)).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Voice error: {e}")
else:
    st.info("Call abhi shuru nahi hui. Start Call dabao.")

if st.session_state.history:
    st.divider()
    for turn in st.session_state.history:
        st.write(f"**User:** {turn['user']}")
        st.write(f"**Ahmed:** {turn['agent']}")
