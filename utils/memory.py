import json
import os
from datetime import datetime

class Memory:
    def __init__(self, storage_path="memory.json"):
        self.storage_path = storage_path
        self.memory = self._load_memory()
    
    def _load_memory(self):
        """加载记忆"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"user_info": {}, "conversations": [], "important_events": []}
        else:
            return {"user_info": {}, "conversations": [], "important_events": []}
    
    def _save_memory(self):
        """保存记忆"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def set_user_info(self, key, value):
        """设置用户信息"""
        self.memory["user_info"][key] = value
        self._save_memory()
    
    def get_user_info(self, key, default=None):
        """获取用户信息"""
        return self.memory["user_info"].get(key, default)
    
    def get_all_user_info(self):
        """获取所有用户信息"""
        return self.memory["user_info"]
    
    def add_conversation(self, user_message, assistant_message):
        """添加对话记录"""
        timestamp = datetime.now().isoformat()
        self.memory["conversations"].append({
            "timestamp": timestamp,
            "user": user_message,
            "assistant": assistant_message
        })
        
        # 只保留最近的100条对话
        if len(self.memory["conversations"]) > 100:
            self.memory["conversations"] = self.memory["conversations"][-100:]
        
        self._save_memory()
    
    def add_important_event(self, event_description):
        """记录重要事件"""
        timestamp = datetime.now().isoformat()
        self.memory["important_events"].append({
            "timestamp": timestamp,
            "description": event_description
        })
        self._save_memory()
    
    def get_recent_conversations(self, limit=5):
        """获取最近的对话"""
        return self.memory["conversations"][-limit:]
    
    def search_memory(self, query):
        """搜索记忆"""
        results = []
        
        # 搜索用户信息
        for key, value in self.memory["user_info"].items():
            if query.lower() in key.lower() or (isinstance(value, str) and query.lower() in value.lower()):
                results.append({"type": "user_info", "key": key, "value": value})
        
        # 搜索对话
        for conv in self.memory["conversations"]:
            if query.lower() in conv["user"].lower() or query.lower() in conv["assistant"].lower():
                results.append({"type": "conversation", "data": conv})
        
        # 搜索重要事件
        for event in self.memory["important_events"]:
            if query.lower() in event["description"].lower():
                results.append({"type": "event", "data": event})
        
        return results