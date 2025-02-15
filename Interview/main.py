import streamlit as st
import pyttsx3
from gpt4all import GPT4All
import tempfile
import os
import re
from ai_feedback import evaluate_answer  
from speech_recognition import start_recording, stop_recording, transcribe_audio  
import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

st.markdown("""
    <style>
        .main {
            max-width: 800px;
            margin: auto;
        }
        .stButton>button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.title("🤖 InterviewMate")

    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}  
    if "transcriptions" not in st.session_state:
        st.session_state.transcriptions = {}  
    if "play_audio" not in st.session_state:
        st.session_state.play_audio = True
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False  
    if "recorded_audio_path" not in st.session_state:
        st.session_state.recorded_audio_path = None  
    if "last_processed_question" not in st.session_state:
        st.session_state.last_processed_question = -1 

    def speak(text):
        """Uses pyttsx3 to speak text aloud."""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    # Start interview
    role = st.text_input("🎯 Enter Job Role:", disabled=st.session_state.interview_started)
    if st.button("🚀 Start Interview", disabled=st.session_state.interview_started):
        try:
            model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
            prompt = f"Provide 5 interview questions for a {role} position."
            questions = model.generate(prompt, max_tokens=200).split("\n")

            st.session_state.questions = [re.sub(r"^\d+\.\s*", "", q.strip()) for q in questions if q.strip()]
            st.session_state.current_q = 0
            st.session_state.interview_started = True
            st.session_state.play_audio = True 
            st.session_state.last_processed_question = -1 
            st.rerun()
        except Exception as e:
            st.error(f"Error generating questions: {e}")

    if st.session_state.interview_started and 0 <= st.session_state.current_q < len(st.session_state.questions):
        question_key = f"question_{st.session_state.current_q}"
        question_text = st.session_state.questions[st.session_state.current_q]

        st.subheader(f"📝 Question {st.session_state.current_q + 1}")
        st.info(question_text)

        if st.session_state.play_audio and st.session_state.last_processed_question != st.session_state.current_q:
            speak(question_text)
            st.session_state.play_audio = False  

        if not st.session_state.is_recording:
            if st.button("🎤 Start Recording"):
                start_recording()
                st.session_state.is_recording = True
                st.rerun()
        else:
            if st.button("🛑 Stop Recording"):
                audio_path = stop_recording()
                st.session_state.is_recording = False

                if audio_path:
                    st.session_state.recorded_audio_path = audio_path  
                    st.session_state.transcriptions[question_key] = transcribe_audio(audio_path)

                    feedback = evaluate_answer(question_text, st.session_state.transcriptions[question_key])
                    st.session_state.answers[question_key] = feedback

                    st.session_state.last_processed_question = st.session_state.current_q

                else:
                    st.warning("⚠ No transcription available. Please try again.")
                st.rerun()

        audio_file = st.file_uploader("📂 Upload your answer:", type=["mp3", "wav", "mp4"], key=question_key)
        
        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
            
            try:
                st.session_state.recorded_audio_path = temp_audio_path
                st.session_state.transcriptions[question_key] = transcribe_audio(temp_audio_path)
                
                feedback = evaluate_answer(question_text, st.session_state.transcriptions[question_key])
                st.session_state.answers[question_key] = feedback

                os.remove(temp_audio_path)
            except Exception as e:
                st.error(f"Error transcribing audio: {e}")

        # Display Previously Processed Data
        if question_key in st.session_state.transcriptions:
            st.write("### 🎙 Transcribed Answer:")
            st.write(st.session_state.transcriptions[question_key])

        if question_key in st.session_state.answers:
            st.write("### 🤖 AI Feedback:")
            st.write(st.session_state.answers[question_key])

        # Navigation Buttons
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.session_state.current_q > 0:
                if st.button("⬅ Back"):
                    st.session_state.current_q -= 1
                    st.session_state.play_audio = False  
                    st.rerun()

        with col2:
            if question_key in st.session_state.answers: 
                if st.button("Next ➡", key="next_button"):
                    st.session_state.current_q += 1
                    st.session_state.play_audio = True  
                    st.rerun()
