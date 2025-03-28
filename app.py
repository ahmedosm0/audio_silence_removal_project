import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import seaborn as sns

# Remove silence parts from raw audio
def remove_silence(audio_path, threshold):
    # Load audio
    audio, sr = librosa.load(audio_path, sr=None)
    
    # Compute non-silent intervals
    non_silent_intervals = librosa.effects.split(audio, top_db=threshold)
    print(f"Non Silent Intervals: {non_silent_intervals}")

    # Concatenate non-silent parts
    output_audio = np.concatenate([audio[start:end] for start, end in non_silent_intervals])
    print(f"Output Audio: {output_audio}")

    # Save processed audio
    output_path = "processed_audio.wav"
    sf.write(output_path, output_audio, sr)
    return output_audio, sr, output_path, audio

# Function to plot waveform
def plot_waveform(audio, sr, title):
    plt.figure(figsize=(10, 4))
    sns.lineplot(x=np.arange(len(audio)) / sr, y=audio, color="blue", linewidth=1.5)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    st.pyplot(plt)  # Streamlit rendering

# Streamlit UI
st.title("Silence Removal from Audio")
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg", "opus"])
threshold = st.slider("Set Silence Threshold", min_value=1, max_value=80, value=15)

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav", start_time=0)

    # Save the uploaded file locally
    with open("uploaded_audio.opus", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the uploaded file
    processed_audio, sr, processed_path, original_audio = remove_silence("uploaded_audio.opus", threshold)
    
    # Plot Uploaded Audio Waveform
    st.write("Uploaded Audio Waveform:")
    plot_waveform(original_audio, sr, title="Uploaded Audio Waveform")

    st.write("Processed audio:")
    st.audio(processed_path, format="audio/wav")

    # Plot Processed Audio Waveform
    st.write("Processed Audio Waveform:")
    plot_waveform(processed_audio, sr, title="Processed Audio Waveform")
