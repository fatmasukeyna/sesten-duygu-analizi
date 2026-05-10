# Speech Emotion Recognition

Bu proje, RAVDESS veri setindeki ses dosyalarindan duygu analizi yapmak icin hazirlandi. Sesler Mel Spectrogram'a cevrilir, CNN modeli egitilir ve yeni bir `.wav` dosyasi icin duygu tahmini yapilir.

## 1. Kurulum

VS Code terminalinde proje klasorune gir:

```powershell
cd "C:\Users\Dell\Documents\New project\speech-emotion-recognition"
```

Sanal ortam olustur:

```powershell
python -m venv .venv
```

Sanal ortami ac:

```powershell
.\.venv\Scripts\Activate.ps1
```

Gerekli kutuphaneleri yukle:

```powershell
pip install -r requirements.txt
```

## 2. Veri Seti

Onerilen veri seti: RAVDESS Emotional Speech Audio.

Kaggle sayfasi:
https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio

Resmi Zenodo kaydi:
https://zenodo.org/records/1188976

Baslangic icin Kaggle'daki sadece konusma seslerini iceren paket daha pratiktir. Indirdikten sonra ZIP dosyasini ac ve `Actor_01`, `Actor_02` gibi klasorleri su klasore yerlestir:

```text
speech-emotion-recognition/data/raw/
```

Beklenen yapi:

```text
data/raw/
  Actor_01/
    03-01-01-01-01-01-01.wav
    ...
  Actor_02/
    ...
```

## 3. Modeli Egitme

```powershell
python src/train.py
```

Egitim sonunda model ve etiket kodlayici `models/` klasorune kaydedilir.

## 4. Tek Ses Dosyasi Tahmini

```powershell
python src/predict.py "data/raw/Actor_01/03-01-03-01-01-01-01.wav"
```

## 5. Arayuzu Calistirma

```powershell
streamlit run app.py
```

Tarayicida acilan sayfadan `.wav` dosyasi yukleyip tahmin alabilirsin.

## RAVDESS Dosya Adi Etiketleri

RAVDESS dosya adlarinda duygu kodu 3. alandadir:

```text
03-01-05-01-02-01-12.wav
      ^^
```

Duygu kodlari:

```text
01 neutral
02 calm
03 happy
04 sad
05 angry
06 fearful
07 disgust
08 surprised
```
