import random
import time

class EmotionSystem:
    def __init__(self):
        # 基本情绪状态
        self.emotions = ["happy", "excited", "calm", "sad", "angry", "flirty", "cute"]
        
        # 情绪转换概率矩阵 (简化版)
        self.transition_probs = {
            "happy": {"happy": 0.7, "excited": 0.1, "calm": 0.1, "flirty": 0.1},
            "excited": {"happy": 0.3, "excited": 0.5, "flirty": 0.2},
            "calm": {"happy": 0.2, "calm": 0.6, "sad": 0.1, "cute": 0.1},
            "sad": {"sad": 0.6, "calm": 0.3, "angry": 0.1},
            "angry": {"angry": 0.5, "calm": 0.3, "sad": 0.2},
            "flirty": {"flirty": 0.6, "happy": 0.2, "excited": 0.2},
            "cute": {"cute": 0.6, "happy": 0.3, "flirty": 0.1}
        }
        
        # 情绪触发词
        self.trigger_words = {
            "happy": ["开心", "高兴", "快乐", "棒", "喜欢", "爱你"],
            "excited": ["太棒了", "好激动", "期待", "兴奋"],
            "calm": ["放松", "平静", "安静", "休息"],
            "sad": ["伤心", "难过", "哭", "不开心", "失望"],
            "angry": ["生气", "烦", "讨厌", "不满", "恼火"],
            "flirty": ["喜欢你", "爱你", "想你", "亲爱", "约会"],
            "cute": ["可爱", "萌", "撒娇", "抱抱"]
        }
        
        # 初始情绪
        self.current_emotion = "happy"
        self.emotion_strength = 0.5  # 0到1之间，表示情绪强度
        self.last_update = time.time()
    
    def get_current_emotion(self):
        """获取当前情绪"""
        # 随着时间推移，情绪会逐渐回归平静
        elapsed_time = time.time() - self.last_update
        if elapsed_time > 300:  # 5分钟无互动
            # 增加回归平静的概率
            if random.random() < 0.3:
                self.current_emotion = "calm"
            self.emotion_strength = max(0.2, self.emotion_strength - 0.1)
            self.last_update = time.time()
        
        return self.current_emotion
    
    def update_emotion(self, user_input, response):
        """根据用户输入和系统回复更新情绪"""
        # 检查触发词
        triggered_emotion = None
        max_matches = 0
        
        for emotion, words in self.trigger_words.items():
            matches = sum(1 for word in words if word in user_input)
            if matches > max_matches:
                max_matches = matches
                triggered_emotion = emotion
        
        # 更新情绪
        if triggered_emotion and max_matches > 0:
            # 根据匹配数量增加情绪强度
            self.emotion_strength = min(1.0, self.emotion_strength + 0.1 * max_matches)
            
            # 根据转换概率矩阵和触发情绪决定新情绪
            if random.random() < self.emotion_strength:
                if triggered_emotion in self.transition_probs[self.current_emotion]:
                    prob = self.transition_probs[self.current_emotion][triggered_emotion]
                    if random.random() < prob:
                        self.current_emotion = triggered_emotion
                else:
                    # 如果当前情绪到触发情绪没有直接转换路径
                    if random.random() < 0.3:
                        self.current_emotion = triggered_emotion
        else:
            # 随机波动
            possible_emotions = list(self.transition_probs[self.current_emotion].keys())
            probs = list(self.transition_probs[self.current_emotion].values())
            
            if random.random() < 0.1:  # 10%概率发生情绪变化
                self.current_emotion = random.choices(possible_emotions, weights=probs)[0]
                self.emotion_strength = max(0.2, self.emotion_strength - 0.1)  # 情绪稍微减弱
        
        self.last_update = time.time()
        return self.current_emotion 