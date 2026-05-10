from __future__ import annotations

import tempfile
from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from src.audio_features import SAMPLE_RATE
from src.predict import predict_emotion_details


EMOTION_TR = {
    "neutral": "Nötr",
    "calm": "Sakin",
    "happy": "Mutlu",
    "sad": "Üzgün",
    "angry": "Kızgın",
    "fearful": "Korku",
    "disgust": "İğrenme",
    "surprised": "Şaşkın",
}


st.set_page_config(page_title="Sesten Duygu Analizi", page_icon="audio", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .metric-card {
        border: 1px solid #d8dee9;
        border-radius: 8px;
        padding: 1rem;
        background: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def save_uploaded_file(uploaded_file) -> Path:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


def plot_waveform(audio_path: Path):
    audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    fig, ax = plt.subplots(figsize=(8, 2.4))
    librosa.display.waveshow(audio, sr=sr, ax=ax, color="#2563eb")
    ax.set_title("Ses Dalga Formu")
    ax.set_xlabel("Süre")
    ax.set_ylabel("Genlik")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return fig


def plot_mel_spectrogram(audio_path: Path):
    audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    mel_db = librosa.power_to_db(mel, ref=np.max)

    fig, ax = plt.subplots(figsize=(8, 3))
    image = librosa.display.specshow(
        mel_db,
        sr=sr,
        x_axis="time",
        y_axis="mel",
        ax=ax,
        cmap="magma",
    )
    ax.set_title("Mel Spectrogram")
    fig.colorbar(image, ax=ax, format="%+2.0f dB")
    fig.tight_layout()
    return fig


def probability_table(probabilities: dict[str, float]) -> pd.DataFrame:
    rows = [
        {"Duygu": EMOTION_TR.get(label, label), "Güven": score}
        for label, score in probabilities.items()
    ]
    return pd.DataFrame(rows).sort_values("Güven", ascending=False)


if "history" not in st.session_state:
    st.session_state.history = []


st.title("Sesten Duygu Analizi")
st.caption("CNN modeli, yüklenen konuşma sesinden duygu tahmini yapar ve modelin kararını görsellerle açıklar.")

left, right = st.columns([0.95, 1.05], gap="large")

with left:
    uploaded_file = st.file_uploader("WAV ses dosyası seç", type=["wav"])

    if uploaded_file is None:
        st.info("Başlamak için bir `.wav` dosyası yükle.")
    else:
        st.audio(uploaded_file, format="audio/wav")

        temp_path = save_uploaded_file(uploaded_file)

        try:
            st.pyplot(plot_waveform(temp_path), use_container_width=True)
        finally:
            plt.close("all")

        if st.button("Duyguyu Tahmin Et", type="primary", use_container_width=True):
            try:
                emotion, confidence, probabilities = predict_emotion_details(temp_path)
                emotion_text = EMOTION_TR.get(emotion, emotion)
                st.session_state.last_result = {
                    "file": uploaded_file.name,
                    "emotion": emotion_text,
                    "confidence": confidence,
                    "probabilities": probabilities,
                    "path": temp_path,
                }
                st.session_state.history.insert(
                    0,
                    {
                        "Dosya": uploaded_file.name,
                        "Tahmin": emotion_text,
                        "Güven": f"{confidence:.2%}",
                    },
                )
                st.session_state.history = st.session_state.history[:5]
            except Exception as exc:
                temp_path.unlink(missing_ok=True)
                st.error(str(exc))

with right:
    result = st.session_state.get("last_result")

    if result is None:
        st.subheader("Analiz sonucu")
        st.write("Tahmin çalıştırıldığında modelin en güçlü duygu tahmini ve sınıf olasılıkları burada görünür.")
    else:
        st.subheader("Analiz sonucu")
        metric_col_1, metric_col_2 = st.columns(2)
        metric_col_1.metric("Tahmin edilen duygu", result["emotion"])
        metric_col_2.metric("Güven oranı", f"{result['confidence']:.2%}")

        probabilities_df = probability_table(result["probabilities"])
        st.bar_chart(probabilities_df, x="Duygu", y="Güven", use_container_width=True)

        try:
            st.pyplot(plot_mel_spectrogram(result["path"]), use_container_width=True)
        except Exception as exc:
            st.warning(f"Spectrogram gösterilemedi: {exc}")
        finally:
            plt.close("all")

if st.session_state.history:
    st.divider()
    st.subheader("Son tahminler")
    st.dataframe(pd.DataFrame(st.session_state.history), hide_index=True, use_container_width=True)
