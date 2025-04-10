from llama_cpp import Llama

llm = Llama(
    model_path="./models/OpenHermes/openhermes-2.5-mistral-7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=32
)

def generate_reply(history):
    output = llm(history, max_tokens=512, stop=["Q:"], temperature=0.7)
    return output["choices"][0]["text"].strip()
