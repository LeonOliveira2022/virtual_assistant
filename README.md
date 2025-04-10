# 🧠 Virtual Girlfriend Assistant

This is a multi-modal virtual assistant that supports both voice and text interaction. It uses OpenAI Whisper for speech recognition, LLaMA GGUF models for language generation, and Microsoft Edge TTS for natural speech synthesis.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/virtual_assistant.git
cd virtual_assistant
```

### 2. Create the Environment

Make sure you have [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

```bash
conda env create -f environment.yml
conda activate vgf
```

### 3. Download the LLaMA GGUF Model

Download a quantized OpenHermes model from Hugging Face:

```bash
mkdir -p ./models/OpenHermes/
wget https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q4_K_M.gguf -O ./models/OpenHermes/openhermes-2.5-mistral-7b.Q4_K_M.gguf
```

> Or place your `.gguf` file manually under `./models/OpenHermes/`.

### 4. Run the Web App

```bash
python web_app.py
```

---

## 📦 Key Dependencies

- `flask` – lightweight web framework
- `whisper` – ASR (automatic speech recognition)
- `edge-tts` – speech synthesis using Microsoft Edge voices
- `llama-cpp-python` – fast LLaMA model inference in GGUF format
- `ffmpeg` – required by Whisper for audio processing

---

## 💡 Notes

- Model replies are either text or voice depending on context.
- Voice messages appear as chat bubbles with playback & transcript buttons.
- Tested on Python 3.10 with Conda on Linux.

---

## 📍 Project Structure

```
virtual_assistant/
├── web_app.py
├── models/
│   ├── chat_model.py
│   └── OpenHermes/
│       └── openhermes-2.5-mistral-7b.Q4_K_M.gguf
├── static/
├── templates/
├── environment.yml
└── README.md
```