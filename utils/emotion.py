# 文件：utils/emotion.py

class EmotionSystem:
    def __init__(self):
        self.current_emotion = "平静"

    def get_current_emotion(self):
        return self.current_emotion

    def update_emotion(self, user_input, response):
        happy_keywords = ["喜欢", "开心", "期待", "嘿嘿", "喵", "爱你", "亲"]
        sad_keywords = ["难过", "想哭", "讨厌", "离开", "生气"]

        if any(kw in response for kw in happy_keywords):
            self.current_emotion = "开心"
        elif any(kw in response for kw in sad_keywords):
            self.current_emotion = "伤心"
        else:
            self.current_emotion = "平静"
