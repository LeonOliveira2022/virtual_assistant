# web_app.py 主路由文件 - 最终版结构
from flask import Flask, render_template, request, jsonify, send_from_directory
import os, uuid, asyncio
from models.asr_model import transcribe_audio
from models.chat_model import generate_reply
from models.tts_model import generate_speech
from utils.emotion import EmotionSystem
from utils.persona import decide_output_type

HISTORY_FILE = "history.txt"
UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

emotion_system = EmotionSystem()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/audio/<path:filename>")
def audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    # 强制加上中文指令提示
    system_prompt = "你是一个说中文的温柔虚拟女友，所有回答都必须使用中文。"

    # 加载历史
    history = system_prompt + "\n"
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history += f.read()

    history += f"Q: {user_input}\nA:"

    try:
        answer = generate_reply(history)
    except Exception as e:
        print("[LLM ERROR]", e)
        answer = "对不起，我刚刚没反应过来呢～"

    history += f" {answer}\n"
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(history)

    # 💡 情绪更新
    emotion_system.update_emotion(user_input, answer)
    emotion = emotion_system.get_current_emotion()

    # 💡 判断输出类型
    output_type = decide_output_type(answer, emotion)

    audio_file = None
    if output_type == "voice":
        audio_file = f"reply_{uuid.uuid4()}.wav"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file)
        try:
            asyncio.run(generate_speech(answer, audio_path))
        except Exception as e:
            print("[ERROR] TTS failed:", e)
            audio_file = None    
    
    return jsonify({
        "message": answer,
        "output_type": output_type,
        "audio_url": f"/audio/{audio_file}" if audio_file else None,
        "emotion": emotion
    })

@app.route("/api/speech-to-text", methods=["POST"])
def speech_to_text():
    uploaded_file = request.files.get('audio')
    if not uploaded_file:
        return jsonify({'error': 'No audio file provided'}), 400

    filename = f"input_{uuid.uuid4().hex}.webm"
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(saved_path)

    try:
        text = transcribe_audio(saved_path)
        return jsonify({"text": text, "file": filename})
    except Exception as e:
        print("[ASR ERROR]", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/get-memory", methods=["GET"])
def get_memory():
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)