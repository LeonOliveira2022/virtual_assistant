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

# 访问根目录"/"时，返回index.html
@app.route("/")
def index():
    return render_template("index.html")

# 访问"/audio"时，返回音频文件
@app.route("/audio/<path:filename>")
def audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 访问"/api/chat"时，处理客户端的POST请求，其他请求比如GET请求会返回405 Method Not Allowed
@app.route("/api/chat", methods=["POST"])
def chat():
    # 将获取的json格式的request.json数据转换为Python字典
    # 如果request不是json格式则request.json返回None
    data = request.json

    # 提取data(python的字典数据)的message字段，如果没有则返回空字符串
    user_input = data.get("message", "")

    # 强制加上中文指令提示
    system_prompt = "你是一个说中文的温柔虚拟女友，所有回答都必须使用中文。"

    # 加载历史
    history = system_prompt + "\n"

    # 如果历史文件存在，则读取历史记录
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history += f.read()

    # 将用户输入添加到历史记录中
    history += f"Q: {user_input}\nA:"

    # 调用chat_model.py中的gernerate_reply()函数，将history作为prompt输入生成回复
    try:
        answer = generate_reply(history)
    # 如果出错了，说明是LLM的问题并返回默认回复
    except Exception as e:
        print("[LLM ERROR]", e)
        answer = "对不起，我刚刚没反应过来呢～"

    # 将LLM生成的回复添加到历史记录中
    history += f" {answer}\n"
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(history)

    # 调用emotion_system的upate_emotion方法更新当前情绪
    emotion_system.update_emotion(user_input, answer)
    emotion = emotion_system.get_current_emotion()

    # 调用persona.py中的decide_output_type()函数判断输出类型
    # 该函数根据模型输出内容和当前情绪来决定输出类型
    output_type = decide_output_type(answer, emotion)


    audio_file = None
    # 如果模型决定输出语音，则调用generate_speech()函数生成语音
    if output_type == "voice":
        # 生成唯一的UUID作为语音文件名
        audio_file = f"reply_{uuid.uuid4()}.wav"
        # 拼接音频文件的完整路径
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file)
        # 异步调用tts_model.py文件中的generate_speech()函数生成语音
        # generate_speech()先根据输入的文本生成语音；然后异步保存到指定路径（写入操作可以异步）
        try:
            asyncio.run(generate_speech(answer, audio_path))
        except Exception as e:
            # 如果出错了，说明是TTS的问题
            print("[ERROR] TTS failed:", e)
            audio_file = None    
    
    # 以json格式返回模型回复消息，输出方式，语音文件地址和情绪
    return jsonify({
        "message": answer,
        "output_type": output_type,
        "audio_url": f"/audio/{audio_file}" if audio_file else None,
        "emotion": emotion
    })

# 语音转文字的路由，处理POST请求（我提交音频文件）
@app.route("/api/speech-to-text", methods=["POST"])
def speech_to_text():
    # request.files.get('audio')获取音频文件
    uploaded_file = request.files.get('audio')
    # 如果音频文件没有上传，则返回错误信息
    if not uploaded_file:
        return jsonify({'error': 'No audio file provided'}), 400

    # 用uuid生成唯一的文件名，保存音频文件到指定目录
    filename = f"input_{uuid.uuid4().hex}.webm"
    # 拼接音频文件的完整路径
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # 保存上传的音频文件到指定目录
    uploaded_file.save(saved_path)

    try:
        text = transcribe_audio(saved_path)
        return jsonify({"text": text, "file": filename})
    except Exception as e:
        print("[ASR ERROR]", e)
        return jsonify({"error": str(e)}), 500

# 获取记忆的路由，获取保存的记忆，不过这个功能暂时在prompt中临时替代一下
@app.route("/api/get-memory", methods=["GET"])
def get_memory():
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)