# -*- coding: utf-8 -*-
"""
Enhanced Chat Analyzer - 深度聊天分析引擎
从有限聊天记录中提取最大逼真度信息
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime


class EnhancedChatAnalyzer:
    """增强版聊天分析器"""
    
    def __init__(self, min_messages: int = 10):
        self.min_messages = min_messages
        
    def analyze(self, messages: List[Dict]) -> Dict:
        """
        综合分析聊天记录
        
        Args:
            messages: [{"timestamp": "...", "sender": "...", "content": "..."}]
            
        Returns:
            完整的分析报告
        """
        if len(messages) < self.min_messages:
            return self._analyze_scarce(messages)
            
        return {
            "personality": self._extract_personality(messages),
            "speaking_style": self._extract_speaking_style(messages),
            "emotional_patterns": self._extract_emotional_patterns(messages),
            "interaction_patterns": self._extract_interaction_patterns(messages),
            "topics_interests": self._extract_topics(messages),
            "inside_jokes": self._extract_inside_jokes(messages),
            "confidence": self._calculate_confidence(messages),
        }
    
    def _analyze_scarce(self, messages: List[Dict]) -> Dict:
        """
        资料不足时的分析策略
        
        逼真度提升策略：
        1. 深度挖掘每条消息的细节
        2. 推断说话者可能的性格特征
        3. 保留更大的"模糊空间"让用户补充
        """
        result = {
            "confidence": "low",
            "message_count": len(messages),
            "personality": {},
            "speaking_style": {},
            "emotional_patterns": {},
            "inference_notes": [],
            "user_input_needed": []
        }
        
        if not messages:
            return result
            
        # 深度分析现有消息
        all_text = " ".join([m.get("content", "") for m in messages])
        
        # 语气词分析（即使只有1条消息）
        particles = self._extract_particles(all_text)
        if particles:
            result["speaking_style"]["particles"] = particles
            result["inference_notes"].append(f"语气词习惯: {particles}")
        
        # 消息长度分析
        avg_len = sum(len(m.get("content", "")) for m in messages) / len(messages)
        result["speaking_style"]["avg_length"] = round(avg_len, 1)
        
        if avg_len > 50:
            result["speaking_style"]["style"] = "长消息者"
        elif avg_len > 20:
            result["speaking_style"]["style"] = "中等长度"
        else:
            result["speaking_style"]["style"] = "短消息者"
            
        # Emoji分析
        emojis = self._extract_emojis(all_text)
        if emojis:
            result["speaking_style"]["emojis"] = emojis[:5]
            
        # 标点习惯
        punctuation = self._extract_punctuation(all_text)
        if punctuation:
            result["speaking_style"]["punctuation"] = punctuation
            
        # 请求用户补充信息
        result["user_input_needed"] = self._get_scarce_input_questions()
        
        return result
    
    def _extract_personality(self, messages: List[Dict]) -> Dict:
        """从聊天记录提取性格特征"""
        target_msgs = [m for m in messages if m.get("content")]
        
        personality = {
            "talkativeness": self._calc_talkativeness(messages),
            "emotional_expressiveness": self._calc_emotional_expressiveness(target_msgs),
            "response_pattern": self._analyze_response_pattern(messages),
            "initiation_style": self._analyze_initiation(messages),
            "personality_traits": [],
        }
        
        # 从消息内容推断性格标签
        all_text = " ".join([m.get("content", "") for m in target_msgs])
        
        # 性格关键词匹配
        trait_keywords = {
            "话痨": ["哈哈", "哈哈哈", "笑死", "太好笑了", "太逗了"],
            "闷骚": ["嗯", "哦", "好吧", "随便", "都行"],
            "温柔": ["好", "可以", "乖", "抱抱", "亲亲"],
            "毒舌": ["切", "哦豁", "得了吧", "搞笑", "无语"],
            "傲娇": ["哼", "才不是", "没有", "谁要", "哼"],
            "体贴": ["注意", "小心", "别", "记得", "要好好"],
            "粘人": ["在吗", "干嘛呢", "想你", "你都不理我"],
            "独立": ["好的", "知道了", "我自己", "没事"],
        }
        
        for trait, keywords in trait_keywords.items():
            match_count = sum(all_text.count(k) for k in keywords)
            if match_count >= 2:
                personality["personality_traits"].append(trait)
                
        return personality
    
    def _extract_speaking_style(self, messages: List[Dict]) -> Dict:
        """提取说话风格"""
        target_msgs = [m for m in messages if m.get("content")]
        all_text = " ".join([m.get("content", "") for m in target_msgs])
        
        return {
            "particles": self._extract_particles(all_text),
            "emojis": self._extract_emojis(all_text)[:10],
            "punctuation": self._extract_punctuation(all_text),
            "typing_patterns": self._extract_typing_patterns(target_msgs),
            "greeting_style": self._extract_greeting_style(messages),
            "closing_style": self._extract_closing_style(messages),
        }
    
    def _extract_emotional_patterns(self, messages: List[Dict]) -> Dict:
        """提取情感模式"""
        target_msgs = [m for m in messages if m.get("content")]
        all_text = " ".join([m.get("content", "") for m in target_msgs])
        
        emotions = {
            "positive": ["开心", "高兴", "喜欢", "爱你", "想你了", "哈哈", "好开心", "棒"],
            "negative": ["生气", "难过", "失望", "委屈", "烦", "讨厌", "哼"],
            "neutral": ["好吧", "嗯", "哦", "这样", "知道了"],
        }
        
        emotion_counts = {"positive": 0, "negative": 0, "neutral": 0}
        
        for emotion_list in [emotions["positive"], emotions["negative"], emotions["neutral"]]:
            key = list(emotions.keys())[list(emotions.values()).index(emotion_list)]
            emotion_counts[key] = sum(all_text.count(e) for e in emotion_list)
        
        total = sum(emotion_counts.values())
        if total > 0:
            emotion_counts = {k: round(v/total*100, 1) for k, v in emotion_counts.items()}
        
        return {
            "distribution": emotion_counts,
            "peak_hours": self._extract_peak_hours(messages),
            "emotional_triggers": self._extract_emotional_triggers(target_msgs),
        }
    
    def _extract_interaction_patterns(self, messages: List[Dict]) -> Dict:
        """提取交互模式"""
        # 谁更主动发消息
        sender_counts = Counter(m.get("sender") for m in messages)
        total = len(messages)
        
        # 平均回复长度
        target_msgs = [m for m in messages if m.get("content")]
        avg_reply_length = sum(len(m.get("content", "")) for m in target_msgs) / len(target_msgs) if target_msgs else 0
        
        # 回复速度（如果有时间戳）
        reply_times = []
        for i in range(1, len(messages)):
            try:
                t1 = datetime.fromisoformat(messages[i-1].get("timestamp", ""))
                t2 = datetime.fromisoformat(messages[i].get("timestamp", ""))
                reply_times.append((t2 - t1).seconds / 60)  # 分钟
            except:
                pass
                
        avg_reply_time = sum(reply_times) / len(reply_times) if reply_times else 0
        
        return {
            "message_ratio": dict(sender_counts),
            "avg_reply_length": round(avg_reply_length, 1),
            "avg_reply_time_minutes": round(avg_reply_time, 1),
            "initiator": max(sender_counts.items(), key=lambda x: x[1])[0] if sender_counts else "unknown",
        }
    
    def _extract_topics(self, messages: List[Dict]) -> Dict:
        """提取话题和兴趣"""
        target_msgs = [m for m in messages if m.get("content")]
        all_text = " ".join([m.get("content", "") for m in target_msgs])
        
        # 话题关键词
        topic_keywords = {
            "美食": ["吃", "做饭", "餐厅", "好吃", "外卖", "火锅", "烧烤"],
            "旅行": ["旅游", "出去玩", "旅行", "机票", "酒店", "景点"],
            "影视": ["电影", "电视剧", "综艺", "刷剧", "追剧"],
            "音乐": ["歌", "音乐", "演唱会", "听歌"],
            "工作": ["上班", "下班", "开会", "工作", "老板", "同事"],
            "学习": ["学习", "考试", "读书", "课程", "上课"],
            "购物": ["买", "购物", "快递", "淘宝", "京东"],
            "健身": ["运动", "健身", "跑步", "瑜伽", "健身房"],
            "八卦": ["听说", "爆料", "朋友说", "有人"],
        }
        
        topics = {}
        for topic, keywords in topic_keywords.items():
            count = sum(all_text.count(k) for k in keywords)
            if count > 0:
                topics[topic] = count
                
        return {
            "detected_topics": topics,
            "top_topics": sorted(topics.items(), key=lambda x: -x[1])[:5] if topics else [],
        }
    
    def _extract_inside_jokes(self, messages: List[Dict]) -> Dict:
        """提取Inside Jokes和特殊表达"""
        target_msgs = [m for m in messages if m.get("content")]
        
        jokes = []
        patterns = [
            r'"[^"]{3,20}"',  # 引号内的内容
            r'【[^】]{3,20}】',  # 括号内内容
            r'叫你[^，,。\s]{1,10}',  # "叫你xxx"
            r'不许[^，,。\s]{1,10}',  # "不许xxx"
            r'每次都[^，,。\s]{1,15}',  # "每次都xxx"
        ]
        
        for msg in target_msgs:
            content = msg.get("content", "")
            for pattern in patterns:
                matches = re.findall(pattern, content)
                jokes.extend(matches)
                
        return {
            "detected": list(set(jokes))[:10],
            "count": len(set(jokes)),
        }
    
    def _calculate_confidence(self, messages: List[Dict]) -> Dict:
        """计算分析置信度"""
        count = len(messages)
        
        if count >= 1000:
            level = "high"
        elif count >= 100:
            level = "medium"
        elif count >= 10:
            level = "low"
        else:
            level = "very_low"
            
        return {
            "level": level,
            "message_count": count,
            "recommendations": self._get_confidence_recommendations(count),
        }
    
    def _get_confidence_recommendations(self, count: int) -> List[str]:
        """获取提升置信度的建议"""
        recommendations = []
        
        if count < 100:
            recommendations.append("建议补充更多聊天记录（至少100条）")
        if count < 500:
            recommendations.append("补充照片可以提升20%逼真度")
        recommendations.append("提供语音消息可分析语速和语气")
        recommendations.append("口述一些特殊记忆和习惯")
        
        return recommendations
    
    def _get_scarce_input_questions(self) -> List[str]:
        """资料不足时需要用户回答的问题"""
        return [
            "ta平时说话比较直接还是委婉？",
            "ta会主动找你聊天吗？频率如何？",
            "ta生气时通常会怎么说？",
            "ta有什么口头禅或习惯用语？",
            "你们之间有什么特别的称呼或暗号？",
            "ta喜欢用什么emoji或表情包？",
        ]
    
    # ========== 辅助分析方法 ==========
    
    def _extract_particles(self, text: str) -> List[Tuple[str, int]]:
        """提取语气词"""
        particle_patterns = [
            "嗯", "哦", "啊", "哈", "呀", "嘛", "呢", "吧", "诶", "唉",
            "噢", "喔", "嗯嗯", "哈哈", "嘿嘿", "对对", "是是"
        ]
        counter = Counter()
        for p in particle_patterns:
            count = text.count(p)
            if count > 0:
                counter[p] = count
        return counter.most_common(10)
    
    def _extract_emojis(self, text: str) -> List[Tuple[str, int]]:
        """提取emoji"""
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
            r'\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF'
            r'\U00002702-\U000027B0\U0000FE00-\U0000FE0F'
            r'\U0001F900-\U0001F9FF]+', re.UNICODE
        )
        emojis = emoji_pattern.findall(text)
        return Counter(emojis).most_common(10)
    
    def _extract_punctuation(self, text: str) -> Dict[str, int]:
        """提取标点使用习惯"""
        return {
            "exclamation": text.count("!") + text.count("！"),
            "question": text.count("?") + text.count("？"),
            "ellipsis": text.count("...") + text.count("…"),
            "comma": text.count(","),
        }
    
    def _extract_typing_patterns(self, messages: List[Dict]) -> Dict:
        """提取打字习惯"""
        patterns = {
            "uses_pinyin_abbrev": False,  # 如"yyds", "xswl"
            "uses_english": False,
            "uses_caps": False,
        }
        
        for msg in messages[:50]:  # 只看前50条
            content = msg.get("content", "")
            if re.search(r'[A-Z]{2,}', content):
                patterns["uses_pinyin_abbrev"] = True
            if re.search(r'[a-zA-Z]{3,}', content):
                patterns["uses_english"] = True
                
        return patterns
    
    def _extract_greeting_style(self, messages: List[Dict]) -> str:
        """提取打招呼风格"""
        greetings = ["在吗", "在不在", "嗨", "hi", "Hey", "你好", "在干嘛"]
        for msg in messages[:20]:
            content = msg.get("content", "")
            for g in greetings:
                if g in content:
                    return g
        return "unknown"
    
    def _extract_closing_style(self, messages: List[Dict]) -> str:
        """提取结束语风格"""
        closings = ["拜拜", "再见", "晚安", "早点睡", "走了", "886"]
        for msg in messages[-20:]:
            content = msg.get("content", "")
            for c in closings:
                if c in content:
                    return c
        return "unknown"
    
    def _calc_talkativeness(self, messages: List[Dict]) -> str:
        """计算话痨程度"""
        avg_len = sum(len(m.get("content", "")) for m in messages) / len(messages)
        if avg_len > 80:
            return "话痨"
        elif avg_len > 30:
            return "适中"
        else:
            return "惜字如金"
    
    def _calc_emotional_expressiveness(self, messages: List[Dict]) -> str:
        """计算情感表达程度"""
        emotional_words = ["爱", "喜欢", "想", "开心", "生气", "难过", "爱你", "想你"]
        all_text = " ".join([m.get("content", "") for m in messages])
        count = sum(all_text.count(w) for w in emotional_words)
        
        if count > len(messages) * 0.3:
            return "丰富"
        elif count > len(messages) * 0.1:
            return "适中"
        else:
            return "内敛"
    
    def _analyze_response_pattern(self, messages: List[Dict]) -> str:
        """分析回复模式"""
        # 简单分析：如果消息普遍较短，可能是被动回复型
        short_msgs = sum(1 for m in messages if len(m.get("content", "")) < 10)
        ratio = short_msgs / len(messages) if messages else 0
        
        if ratio > 0.6:
            return "被动简洁型"
        elif ratio > 0.3:
            return "互动均衡型"
        else:
            return "主动分享型"
    
    def _analyze_initiation(self, messages: List[Dict]) -> str:
        """分析主动程度"""
        # 简单实现：看消息开头是否有问句
        questions = sum(1 for m in messages if "？" in m.get("content", "") or "?" in m.get("content", ""))
        ratio = questions / len(messages) if messages else 0
        
        if ratio > 0.4:
            return "主动型"
        elif ratio > 0.2:
            return "均衡型"
        else:
            return "被动型"
    
    def _extract_peak_hours(self, messages: List[Dict]) -> List[int]:
        """提取活跃时间段"""
        hours = []
        for msg in messages:
            try:
                ts = msg.get("timestamp", "")
                if ts:
                    hour = datetime.fromisoformat(ts).hour
                    hours.append(hour)
            except:
                pass
        if not hours:
            return []
        return [h for h, _ in Counter(hours).most_common(3)]
    
    def _extract_emotional_triggers(self, messages: List[Dict]) -> List[str]:
        """提取情绪触发点"""
        triggers = []
        
        trigger_patterns = [
            (["生气", "烦", "怒"], "负面触发词"),
            (["开心", "高兴", "棒"], "正面触发词"),
            (["为什么", "怎么回事", "?"], "疑问场景"),
        ]
        
        all_text = " ".join([m.get("content", "") for m in messages])
        
        for words, label in trigger_patterns:
            if any(any(w in msg.get("content", "") for w in words) for msg in messages):
                triggers.append(label)
                
        return triggers


def main():
    """测试用"""
    analyzer = EnhancedChatAnalyzer()
    
    # 模拟少量数据
    test_messages = [
        {"timestamp": "2024-01-01 10:00:00", "sender": "妈妈", "content": "起床了吗"},
        {"timestamp": "2024-01-01 10:30:00", "sender": "妈妈", "content": "记得吃早饭哦"},
        {"timestamp": "2024-01-01 20:00:00", "sender": "妈妈", "content": "在干嘛呢"},
    ]
    
    result = analyzer.analyze(test_messages)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
