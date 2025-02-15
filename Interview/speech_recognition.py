import sounddevice as sd
import numpy as np
import wave
import whisper
import tempfile
import threading
import time

recording = []
is_recording = False
samplerate = 16000  
channels = 1

def callback(indata, frames, time, status):
    """Callback function to store recorded data."""
    if status:
        print(f"Error: {status}")
    if is_recording:
        recording.append(indata.copy())

def start_recording():
    """Starts recording audio manually."""
    global is_recording, recording
    is_recording = True
    recording = []  

    def record():
        with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback, dtype="int16"):
            print("Recording started... Speak now!")
            while is_recording:
                sd.sleep(100) 

    threading.Thread(target=record, daemon=True).start()

def stop_recording():
    """Stops recording and saves it to a temporary file."""
    global is_recording
    is_recording = False
    print("Recording stopped.")

    if not recording:
        print("No audio recorded.")
        return None

    recorded_audio = np.concatenate(recording, axis=0) 

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio_path = temp_audio.name

    with wave.open(temp_audio_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  
        wf.setframerate(samplerate)
        wf.writeframes(recorded_audio.tobytes())

    print(f"Saved recording to: {temp_audio_path}")
    return temp_audio_path 

def transcribe_audio(file_path):
    """Transcribes an audio file using Whisper."""
    model = whisper.load_model("base")
    print("Transcribing audio...")
    result = model.transcribe(file_path)
    print("Transcription complete.")
    return result["text"]

if __name__ == "__main__":
    start_recording()
    time.sleep(5)  
    audio_file = stop_recording()

    if audio_file:
        transcript = transcribe_audio(audio_file)
        print("Transcription:", transcript)
    else:
        print("No audio was recorded.")

    print("Script execution finished.")
