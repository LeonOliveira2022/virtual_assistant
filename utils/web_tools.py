import requests
import json
import re
import random

class WebTools:
    def __init__(self, debug_mode=True):
        # API URLs
        self.search_engine_url = "https://api.example.com/search"
        self.music_api_url = "https://api.example.com/music"
        self.news_api_url = "https://api.example.com/news"
        self.weather_api_url = "https://api.example.com/weather"
        
        self.debug_mode = debug_mode  # 切换模拟/真实数据
        self.api_keys = {
            "search": "your_search_api_key",
            "music": "your_music_api_key",
            "news": "your_news_api_key",
            "weather": "your_weather_api_key"
        }

    def search(self, query):
        """根据用户输入进行信息搜索"""
        keywords = re.sub(r'(搜索|查询|查找|帮我找|告诉我关于)', '', query).strip()
        if not keywords:
            return "我没能识别你想搜索的关键词哦～"

        try:
            if not self.debug_mode:
                response = requests.get(
                    self.search_engine_url,
                    params={"q": keywords, "apiKey": self.api_keys["search"]}
                )
                return response.text  # 或提取结果格式化返回

            # 模拟返回结果
            return f"关于「{keywords}」的搜索结果：这是一些相关信息，例如百科介绍、最新资讯或相关链接。"

        except Exception as e:
            return f"搜索失败：{str(e)}"

    def recommend_music(self, query):
        """根据语义推荐音乐"""
        music_type = next((k for k in ["流行", "摇滚", "民谣", "古典", "电子", "嘻哈", "轻音乐"] if k in query), None)
        mood = next((k for k in ["开心", "兴奋", "放松", "伤感", "浪漫", "励志"] if k in query), None)

        try:
            if not self.debug_mode:
                params = {"apiKey": self.api_keys["music"]}
                if music_type:
                    params["genre"] = music_type
                if mood:
                    params["mood"] = mood
                response = requests.get(self.music_api_url, params=params)
                return response.text

            music_data = {
                "流行": ["周杰伦《稻香》", "Adele《Hello》"],
                "摇滚": ["Beyond《海阔天空》"],
                "民谣": ["陈粒《易燃易爆炸》"],
                "古典": ["贝多芬《月光奏鸣曲》"],
                "电子": ["Avicii《Wake Me Up》"],
                "嘻哈": ["Eminem《Lose Yourself》"],
                "轻音乐": ["Yiruma《River Flows in You》"]
            }

            mood_data = {
                "开心": ["Pharrell Williams《Happy》"],
                "兴奋": ["Queen《We Will Rock You》"],
                "放松": ["Ed Sheeran《Perfect》"],
                "伤感": ["Adele《Someone Like You》"],
                "浪漫": ["Bruno Mars《Just The Way You Are》"],
                "励志": ["Katy Perry《Roar》"]
            }

            if music_type and music_type in music_data:
                return random.choice(music_data[music_type])
            elif mood and mood in mood_data:
                return random.choice(mood_data[mood])
            else:
                return random.choice(["周杰伦《七里香》", "林俊杰《江南》", "Lady Gaga《Bad Romance》"])

        except Exception as e:
            return f"音乐推荐失败：{str(e)}"

    def get_weather(self, location="深圳"):
        """获取天气描述信息"""
        try:
            if not self.debug_mode:
                response = requests.get(
                    self.weather_api_url,
                    params={"location": location, "apiKey": self.api_keys["weather"]}
                )
                return response.text

            conditions = ["晴朗", "多云", "小雨", "阴天", "大雨", "雷阵雨"]
            temperature = random.randint(10, 35)
            condition = random.choice(conditions)
            return f"{location}今天天气{condition}，气温约{temperature}℃。"

        except Exception as e:
            return f"获取天气失败：{str(e)}"

    def get_news(self, category=None):
        """获取新闻摘要"""
        categories = ["科技", "娱乐", "体育", "社会", "国际", "财经"]
        if not category:
            category = random.choice(categories)

        try:
            if not self.debug_mode:
                response = requests.get(
                    self.news_api_url,
                    params={"category": category, "apiKey": self.api_keys["news"]}
                )
                return response.text

            news_pool = [
                "新一代AI模型引发科技热潮。",
                "国际社会聚焦气候问题。",
                "本地高校研发出新型储能电池。",
                "明星婚礼引发粉丝狂欢。",
                "世界杯激战正酣，观众热情高涨。"
            ]
            return f"今日{category}新闻：{random.choice(news_pool)}"

        except Exception as e:
            return f"获取新闻失败：{str(e)}"
