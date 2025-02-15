import streamlit as st
import pyttsx3
from gpt4all import GPT4All
import whisper
import tempfile
import os
import re

st.title("AI Personal Interviewer Assistant")

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

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

role = st.text_input("Enter Job Role:")
if st.button("Start Interview"):
    try:
        model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
        prompt = f"Provide 5 interview questions for a {role} position."
        questions = model.generate(prompt, max_tokens=200).split("\n")

        st.session_state.questions = [re.sub(r"^\d+\.\s*", "", q.strip()) for q in questions if q.strip()]
        st.session_state.current_q = 0
        st.session_state.interview_started = True
        st.session_state.play_audio = True 
        
    except Exception as e:
        st.error(f"Error generating questions: {e}")

if st.session_state.interview_started and 0 <= st.session_state.current_q < len(st.session_state.questions):
    question_key = f"question_{st.session_state.current_q}"
    question_text = st.session_state.questions[st.session_state.current_q]

    st.write(f"### Question {st.session_state.current_q + 1}: {question_text}")

    if st.session_state.play_audio:
        speak(question_text)
        st.session_state.play_audio = False  

    previous_audio = st.session_state.answers.get(question_key, None)
    previous_text = st.session_state.transcriptions.get(question_key, "")

    audio_file = st.file_uploader(
        "Upload your answer:", type=["mp3", "wav", "mp4"], key=question_key
    )

    if audio_file:
        st.session_state.answers[question_key] = audio_file
        st.audio(audio_file)  

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name

        try:
            model = whisper.load_model("base")
            result = model.transcribe(temp_audio_path)

            if "text" in result:
                st.session_state.transcriptions[question_key] = result["text"]
                st.write("### Transcribed Answer:")
                st.write(result["text"])  

            os.remove(temp_audio_path)

        except Exception as e:
            st.error(f"Error transcribing audio: {e}")

    elif previous_audio:
        st.audio(previous_audio)
        if previous_text:
            st.write("### Transcribed Answer:")
            st.write(previous_text)

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.current_q > 0 and st.button("Back"):
            st.session_state.current_q -= 1
            st.session_state.play_audio = False  
            st.rerun()

    with col2:
        if st.session_state.current_q < len(st.session_state.questions) - 1:
            if question_key in st.session_state.transcriptions:
                if st.button("Next"):
                    st.session_state.current_q += 1
                    st.session_state.play_audio = True  
                    st.rerun()
