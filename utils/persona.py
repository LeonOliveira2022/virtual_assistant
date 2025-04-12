# 文件：utils/persona.py

def decide_output_type(response, emotion):
    score = 0

    # 情绪判断
    if emotion in ["开心", "撒娇", "调皮"]:
        score += 2
    elif emotion in ["平静", "伤心"]:
        score -= 1

    # 回复长度判断
    if len(response) < 40:
        score += 1
    elif len(response) > 100:
        score -= 1

    # 亲昵语句判断（由模型判断）
    if is_affectionate(response):
        score += 2

    return "voice" if score >= 2 else "text"

def is_affectionate(response):
    # 通过语言模型判断
    prompt = f"""请判断下面这句话是否带有亲昵、温柔或感情丰富的语气？只回答“是”或“否”：
“{response}”"""
    from llama_cpp import Llama
    llm = Llama(model_path="./models/OpenHermes/openhermes-2.5-mistral-7b.Q4_K_M.gguf", n_ctx=2048, n_threads=8, n_gpu_layers=32)
    result = llm(prompt, max_tokens=10)
    text = result["choices"][0]["text"].strip()
    return text.startswith("是")
