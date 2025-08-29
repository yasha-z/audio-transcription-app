import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io

st.title("Audio Transcription App")
st.write("Upload an audio file (MP3, MPEG, WAV, OGG, M4A) to transcribe it.")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "mpeg", "wav", "ogg", "m4a"])
CHUNK_LENGTH_S = 30

if uploaded_file is not None:
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) // 1000  # duration in seconds
    full_transcript = []
    num_chunks = duration // CHUNK_LENGTH_S + 1
    progress_bar = st.progress(0)
    st.write(f"Processing {num_chunks} chunks...")

    for idx, i in enumerate(range(0, duration, CHUNK_LENGTH_S)):
        chunk = audio[i*1000:(i+CHUNK_LENGTH_S)*1000]
        wav_bytes = io.BytesIO()
        chunk.export(wav_bytes, format="wav")
        wav_bytes.seek(0)
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                full_transcript.append(text)
            except sr.UnknownValueError:
                full_transcript.append("[Unrecognized audio]")
            except sr.RequestError as e:
                full_transcript.append(f"[API error: {e}]")
        progress_bar.progress((idx + 1) / num_chunks)

    final_text = " ".join(full_transcript)
    st.subheader("Transcript:")
    st.text_area("Transcription", final_text, height=300)
    st.download_button("Download Transcript", final_text, file_name="transcript.txt")
