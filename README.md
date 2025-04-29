---

# 🧠 Lyra: A Multimodal AI Assistant

Lyra is a multimodal virtual assistant that supports **both voice and text interactions**.  
It integrates OpenAI Whisper for speech recognition, a LLaMA GGUF (Q4 quantized) model for language generation, and Microsoft Edge TTS for natural speech synthesis, aiming to deliver a smooth and natural conversational experience.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/lyra.git
cd lyra
```

### 2. Create the Environment

Make sure you have [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

```bash
conda env create -f environment.yml
conda activate lyra
```

### 3. Download the LLaMA GGUF Model

Download the quantized OpenHermes model from Hugging Face:

```bash
mkdir -p ./models/OpenHermes/
wget https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q4_K_M.gguf -O ./models/OpenHermes/openhermes-2.5-mistral-7b.Q4_K_M.gguf
```

> Alternatively, you can manually place the `.gguf` file in the `./models/OpenHermes/` directory.

### 4. Launch the Web Application

```bash
python web_app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to start interacting.

---

## 📦 Key Dependencies

- `flask` — lightweight web framework
- `whisper` — automatic speech recognition (ASR)
- `edge-tts` — text-to-speech synthesis via Microsoft Edge
- `llama-cpp-python` — fast inference for LLaMA GGUF models
- `ffmpeg` — audio processing tool required by Whisper

---

## 💡 Key Features

- **Multimodal Interaction**: Supports both text and voice input; intelligently selects text or voice output based on context.
- **Natural Voice Experience**: Voice replies are displayed as chat bubbles with playback and transcription options.
- **Efficient Local Deployment**: Smooth operation on consumer-grade GPUs (e.g., RTX 3060 recommended, 12GB VRAM or higher).

---

## 📍 Project Structure

```
lyra/
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

---

## 📢 Disclaimer

Lyra is an experimental open-source project focused on exploring multimodal interaction technologies.  
Feel free to extend and customize it according to your needs.

---