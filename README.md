# InterviewMate Personal Interview Assistant

## Overview
InterviewMate is a Streamlit-based application designed to help users practice for job interviews. It generates interview questions based on a given job role, allows users to record or upload their answers, transcribes audio responses, and provides AI-powered feedback to improve their interview performance.

## Features
- Generate interview questions tailored to a specified job role.
- Text-to-speech functionality to read out questions.
- Audio recording and transcription of responses.
- AI-generated feedback on user responses.
- Navigation between questions for a seamless interview experience.

## Technologies Used
- **Python**
- **Streamlit** (UI Framework)
- **GPT4All** (Question Generation)
- **Pyttsx3** (Text-to-Speech)
- **Whisper** (Speech-to-Text)
- **Torch** (Machine Learning Backend)
- **Tempfile & OS** (File Handling)

## Installation
1. Clone the repository
2. Install dependencies:
   pip install streamlit gpt4all pyttsx3 whisper torch
3. Run the application:
   streamlit run app.py

## Usage
1. Enter the job role in the input field.
2. Click the "Start Interview" button to generate questions.
3. Answer questions by either recording or uploading an audio response.
4. View transcriptions and receive AI-generated feedback.
5. Navigate between questions using the "Next" and "Back" buttons.

## Future Improvements
- Integration with more AI models for enhanced feedback.
- Support for additional languages.
- Improved UI/UX enhancements.

## Contributors
- [Jerome Victoria](https://github.com/1Jerome23)



