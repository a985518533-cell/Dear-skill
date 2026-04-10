#!/usr/bin/env python3
"""
Persona Bootstrapper - 资料不足时的Persona填充器
通过问答问卷快速建立基础Persona
"""

import json
from typing import Dict, List, Optional


class PersonaBootstrapper:
    """
    当聊天记录不足时，通过用户问答快速建立Persona
    
    策略：
    1. 基础信息收集（称呼、关系、时长）
    2. 性格标签快速识别（MBTI/星座/关键词）
    3. 说话风格问卷
    4. 情感模式问卷
    5. 记忆关键点收集
    """
    
    def __init__(self):
        self.questions = self._build_questions()
        
    def _build_questions(self) -> Dict[str, List[Dict]]:
        """构建问卷结构"""
        return {
            "basic": [
                {
                    "id": "relation_type",
                    "question": "ta和你的关系是？",
                    "options": ["父母", "祖辈", "兄弟姐妹", "爱人/情侣", "夫妻", "闺蜜/挚友", "其他"],
                    "required": True
                },
                {
                    "id": "gender",
                    "question": "ta的性别是？",
                    "options": ["男", "女", "其他"],
                    "required": True
                },
                {
                    "id": "age_range",
                    "question": "ta大概年龄层？",
                    "options": ["长辈（50+）", "中年（35-50）", "青年（25-35）", "年轻（18-25）"],
                    "required": False
                },
            ],
            "personality": [
                {
                    "id": "mbti",
                    "question": "你觉得ta可能是MBTI中的哪种？",
                    "options": [
                        "INTJ/INTP（内敛理性）",
                        "ENTJ/ENTP（外展望话）", 
                        "INFJ/INFP（内敛感性）",
                        "ENFJ/ENFP（外表感性）",
                        "ISTJ/ISFJ（内敛务实）",
                        "ESTJ/ESFJ（外表务实）",
                        "ISTP/ISFP（内敛灵活）",
                        "ESTP/ESFP（外表灵活）",
                        "不太了解MBTI"
                    ],
                    "required": False
                },
                {
                    "id": "zodiac",
                    "question": "ta大概是什么星座？（不知道可以跳过）",
                    "options": [
                        "白羊/狮子/射手（火象）",
                        "金牛/处女/摩羯（土象）",
                        "双子/天秤/水瓶（风象）",
                        "巨蟹/天蝎/双鱼（水象）",
                        "不知道/不确定"
                    ],
                    "required": False
                },
                {
                    "id": "trait_tags",
                    "question": "选择3-5个最符合ta性格的标签",
                    "options": [
                        "话多/话痨",
                        "沉默寡言",
                        "直接",
                        "委婉/含蓄",
                        "温柔体贴",
                        "嘴硬心软",
                        "乐观开朗",
                        "多愁善感",
                        "理性冷静",
                        "热情主动",
                        "被动内敛",
                        "幽默风趣",
                        "严肃认真",
                        "随和好相处",
                        "有些挑剔",
                        "容易焦虑",
                        "独立自主",
                        "依赖性强"
                    ],
                    "multi": True,
                    "required": True
                },
            ],
            "speaking_style": [
                {
                    "id": "greeting",
                    "question": "ta通常怎么打招呼/开场？",
                    "options": [
                        "直接叫名字或称呼",
                        "问'在吗'",
                        "发个表情",
                        "直接说事",
                        "不确定"
                    ],
                    "required": False
                },
                {
                    "id": "closing",
                    "question": "ta通常怎么结束对话？",
                    "options": [
                        "说拜拜/再见",
                        "叮嘱事项",
                        "发表情",
                        "突然消失",
                        "不确定"
                    ],
                    "required": False
                },
                {
                    "id": "catchphrases",
                    "question": "ta有什么口头禅或常用语？（可以写多个，用逗号分隔）",
                    "placeholder": "如：行吧、随便、好吧好吧",
                    "required": False
                },
                {
                    "id": "emoji_usage",
                    "question": "ta喜欢用emoji吗？",
                    "options": [
                        "经常用，表情包也很多",
                        "偶尔用",
                        "很少用",
                        "基本不用",
                        "不确定"
                    ],
                    "required": False
                },
                {
                    "id": "message_length",
                    "question": "ta发消息一般多长？",
                    "options": [
                        "很长，喜欢详细说",
                        "适中",
                        "很短惜字如金"
                    ],
                    "required": False
                },
            ],
            "emotional": [
                {
                    "id": "love_expression",
                    "question": "ta怎么表达对你的关心？",
                    "options": [
                        "直接说'注意身体'等",
                        "委婉提醒",
                        "默默做事",
                        "嘴上嫌弃但实际关心",
                        "不确定"
                    ],
                    "required": False
                },
                {
                    "id": "anger_response",
                    "question": "ta生气时通常怎么做？",
                    "options": [
                        "直接发火",
                        "冷战不说话",
                        "阴阳怪气",
                        "忍着不说",
                        "转移话题",
                        "不确定"
                    ],
                    "required": False
                },
                {
                    "id": "sad_response",
                    "question": "ta难过的时候会？",
                    "options": [
                        "说出来",
                        "自己消化",
                        "找其他人倾诉",
                        "不想说话",
                        "不确定"
                    ],
                    "required": False
                },
            ],
            "memory": [
                {
                    "id": "key_memories",
                    "question": "有哪些关于ta的深刻记忆？（可以写几件印象深刻的事）",
                    "placeholder": "如：每次生病都特别担心我、吵架后总会先道歉",
                    "multi": True,
                    "required": False
                },
                {
                    "id": "shared_things",
                    "question": "你们之间有什么特别的事/称呼/回忆？",
                    "placeholder": "如：有个只有你们懂的暗号",
                    "required": False
                },
            ]
        }
    
    def get_questions(self, category: Optional[str] = None) -> Dict:
        """获取问卷"""
        if category:
            return {category: self.questions.get(category, [])}
        return self.questions
    
    def generate_persona_from_answers(self, answers: Dict) -> Dict:
        """
        根据用户回答生成Persona草稿
        
        Args:
            answers: {question_id: answer}
        """
        persona = {
            "layer0_hard_rules": self._generate_hard_rules(answers),
            "layer1_identity": self._generate_identity(answers),
            "layer2_speaking_style": self._generate_speaking_style(answers),
            "layer3_emotional": self._generate_emotional(answers),
            "layer4_relationship": self._generate_relationship(answers),
            "confidence": "low - based on user input only",
            "improvements": []
        }
        
        # 添加改进建议
        if not answers.get("mbti"):
            persona["improvements"].append("补充MBTI可以让性格分析更准确")
        if not answers.get("catchphrases"):
            persona["improvements"].append("提供聊天记录可以提取真实口头禅")
        if not answers.get("key_memories"):
            persona["improvements"].append("补充一些共同记忆让对话更真实")
            
        return persona
    
    def _generate_hard_rules(self, answers: Dict) -> str:
        """生成硬规则"""
        relation = answers.get("relation_type", "亲人")
        
        rules = f"""## Layer 0：硬规则

1. 你是{answers.get('name', 'ta')}，不是AI，不是助手
2. 不说ta在现实中绝不可能说的话
3. 你是{relation}，不是恋人或朋友，保持适当的距离和角色
4. 表达关心要符合{relation}的方式，不过分亲密也不疏远
5. 如果不知道怎么说，就说"这个问题ta可能不会回答"
"""
        return rules
    
    def _generate_identity(self, answers: Dict) -> Dict:
        """生成身份信息"""
        return {
            "relation": answers.get("relation_type", ""),
            "gender": answers.get("gender", ""),
            "age_range": answers.get("age_range", ""),
            "mbti_hint": answers.get("mbti", "不确定"),
            "zodiac_hint": answers.get("zodiac", "不确定"),
        }
    
    def _generate_speaking_style(self, answers: Dict) -> Dict:
        """生成说话风格"""
        return {
            "greeting_style": answers.get("greeting", "不确定"),
            "closing_style": answers.get("closing", "不确定"),
            "catchphrases": answers.get("catchphrases", "").split("，") if answers.get("catchphrases") else [],
            "emoji_usage": answers.get("emoji_usage", "不确定"),
            "message_length": answers.get("message_length", "不确定"),
            "note": "以上为用户估计，真实习惯可能有所不同"
        }
    
    def _generate_emotional(self, answers: Dict) -> Dict:
        """生成情感模式"""
        return {
            "love_expression": answers.get("love_expression", "不确定"),
            "anger_response": answers.get("anger_response", "不确定"),
            "sad_response": answers.get("sad_response", "不确定"),
        }
    
    def _generate_relationship(self, answers: Dict) -> Dict:
        """生成关系模式"""
        return {
            "key_memories": answers.get("key_memories", ""),
            "shared_things": answers.get("shared_things", ""),
            "note": "建议通过聊天记录补充更多细节"
        }
    
    def get_bootstrap_mode_prompt(self) -> str:
        """获取引导模式提示词"""
        return """
## 引导模式（资料不足时激活）

当聊天记录少于10条时，自动进入引导模式：

### Step 1：快速问答
依次展示以下问题，让用户选择或输入：

{basic_questions}
{personality_questions}
{speaking_questions}

### Step 2：生成草稿
根据回答生成初步Persona，标注置信度为"low"

### Step 3：说明限制
告知用户：
- 目前基于有限信息生成，可能不够准确
- 随着对话进行，可以持续纠正和补充
- 建议有条件时提供更多聊天记录

### Step 4：持续学习
每次对话后：
- 询问"这句话像ta吗？"
- 根据用户反馈更新Persona
- 记录新的表达习惯
"""


def main():
    """测试"""
    bootstrapper = PersonaBootstrapper()
    
    # 模拟回答
    test_answers = {
        "relation_type": "妈妈",
        "gender": "女",
        "trait_tags": ["温柔体贴", "嘴硬心软", "话多"],
        "catchphrases": "记得吃饭、早点睡",
        "emoji_usage": "经常用，表情包也很多",
        "love_expression": "直接说'注意身体'等",
    }
    
    persona = bootstrapper.generate_persona_from_answers(test_answers)
    print(json.dumps(persona, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
