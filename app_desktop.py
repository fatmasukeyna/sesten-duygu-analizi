from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from src.predict import predict_emotion


EMOTION_TR = {
    "neutral": "Notr",
    "calm": "Sakin",
    "happy": "Mutlu",
    "sad": "Uzgun",
    "angry": "Kizgin",
    "fearful": "Korku",
    "disgust": "Igrenme",
    "surprised": "Saskin",
}


class EmotionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sesten Duygu Analizi")
        self.geometry("520x320")
        self.minsize(520, 320)
        self.configure(bg="#f4f6f8")

        self.selected_file: Path | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        title = tk.Label(
            self,
            text="Sesten Duygu Analizi",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6f8",
            fg="#17202a",
        )
        title.pack(pady=(28, 8))

        self.file_label = tk.Label(
            self,
            text="Henuz ses dosyasi secilmedi",
            font=("Segoe UI", 10),
            bg="#f4f6f8",
            fg="#52616b",
            wraplength=450,
        )
        self.file_label.pack(pady=(0, 18))

        button_frame = tk.Frame(self, bg="#f4f6f8")
        button_frame.pack(pady=6)

        select_button = tk.Button(
            button_frame,
            text="Ses Dosyasi Sec",
            command=self.select_file,
            width=18,
            height=2,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
        )
        select_button.grid(row=0, column=0, padx=8)

        predict_button = tk.Button(
            button_frame,
            text="Tahmin Et",
            command=self.predict,
            width=18,
            height=2,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
        )
        predict_button.grid(row=0, column=1, padx=8)

        self.result_label = tk.Label(
            self,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f6f8",
            fg="#111827",
        )
        self.result_label.pack(pady=(32, 4))

        self.confidence_label = tk.Label(
            self,
            text="",
            font=("Segoe UI", 12),
            bg="#f4f6f8",
            fg="#52616b",
        )
        self.confidence_label.pack()

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Ses dosyasi sec",
            filetypes=[("WAV dosyalari", "*.wav"), ("Tum dosyalar", "*.*")],
        )

        if file_path:
            self.selected_file = Path(file_path)
            self.file_label.config(text=str(self.selected_file))
            self.result_label.config(text="")
            self.confidence_label.config(text="")

    def predict(self) -> None:
        if self.selected_file is None:
            messagebox.showwarning("Dosya secilmedi", "Once bir .wav ses dosyasi secmelisin.")
            return

        try:
            self.result_label.config(text="Tahmin yapiliyor...")
            self.confidence_label.config(text="")
            self.update_idletasks()

            emotion, confidence = predict_emotion(self.selected_file)
            emotion_text = EMOTION_TR.get(emotion, emotion)

            self.result_label.config(text=f"Tahmin: {emotion_text}")
            self.confidence_label.config(text=f"Guven orani: {confidence:.2%}")
        except Exception as exc:
            self.result_label.config(text="")
            self.confidence_label.config(text="")
            messagebox.showerror("Hata", str(exc))


if __name__ == "__main__":
    app = EmotionApp()
    app.mainloop()
