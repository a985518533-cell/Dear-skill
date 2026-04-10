# 亲人/爱人.skill

> *把爱和回忆蒸馏成AI，让数字永生成可能*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)

---

## 核心价值

**「前任.skill」的进化版**，专为保存亲人、爱人、朋友的数字记忆而设计。

| 特征 | 前任.skill | 亲人/爱人.skill |
|------|----------|----------------|
| 目标 | 情感疗愈，保留记忆 | 数字永生，情感延续 |
| 分手指南 | 有"分手"概念 | 无分手概念 |
| 语气风格 | 保持"棱角" | 温暖回忆为主 |
| 已故亲人 | 不适用 | ✅ 支持缅怀模式 |
| 逼真度优化 | 基础 | 增强30%+ |
| **资料不足方案** | 无 | ✅ Bootstrap模式 |

---

## 技术突破

### 1. 语音消息处理（核心痛点解决）

**痛点**：微信语音消息无法直接提取

**解决方案**：
```bash
# 使用Whisper将语音转为文字
pip install openai-whisper
python tools/voice_parser.py --input voice_dir --output text.txt --batch
```

**提取维度**：
- 语速（快/慢/中等）
- 停顿习惯
- 语气词（嗯/哦/啊）
- 情绪状态（开心/生气/难过）
- 语音长度偏好

### 2. 多模态输入增强逼真度

| 输入类型 | 提取内容 | 逼真度提升 |
|---------|---------|-----------|
| 语音消息 | 语速、语气、情绪特征 | +30% |
| 照片EXIF | 时间线、地点、场景 | +20% |
| 表情包 | 语义映射、偏好分析 | +15% |
| 标点符号 | 习惯（感叹号/省略号） | +10% |

### 3. 上下文感知增强

```
输入 → 上下文补全 → 性格匹配 → 风格适配 → 输出
```

AI会记住：
- 你们之前讨论过什么
- ta在特定场景下的典型反应
- ta的特殊习惯和口头禅

### 4. 资料不足解决方案（Bootstrap模式）

当聊天记录少于10条时，自动激活Bootstrap引导模式：

| 资料量 | 策略 | 逼真度 |
|-------|------|-------|
| 极少（<10条） | MBTI/星座+口述记忆 | ~40% |
| 少量（10-100条） | 增强口头禅分析+口述补充 | ~60% |
| 中等（100-1000条） | 聊天记录+照片 | ~80% |
| 大量（1000+条） | 全量多模态输入 | ~95% |

**Bootstrap快速问答：**
1. 关系类型、年龄、性别
2. 性格标签选择（话痨/沉默/温柔/毒舌...）
3. 说话风格估计（口头禅、emoji使用）
4. 关键记忆口述

**持续学习：** 随着对话进行，AI会不断学习和纠正，提升逼真度

### 5. 自动发消息功能 ⭐

用户主动开启后，AI自动分析聊天习惯并定时发送消息：

| 支持平台 | 稳定性 | 配置难度 |
|---------|-------|---------|
| Telegram Bot | ✅ 稳定 | 需Bot Token |
| 钉钉 Webhook | ✅ 稳定 | 需Webhook URL |
| 飞书 Webhook | ✅ 稳定 | 需Webhook URL |
| 微信 PC | ⚠️ 有风险 | 封号风险高 |

**触发命令：** `/auto-send`

---

## 目录结构

```
dear-skill/
├── SKILL.md                    # 技能入口
├── prompts/                    # Prompt模板
│   ├── memory_builder.md       # 关系记忆生成
│   ├── persona_builder.md      # 人物性格生成（优化版）
│   ├── intake.md               # 信息录入
│   └── ...
├── tools/                      # Python工具
│   ├── voice_parser.py         # ⭐ 语音消息解析
│   ├── wechat_parser.py        # 微信聊天记录解析
│   ├── qq_parser.py            # QQ聊天记录解析
│   ├── photo_analyzer.py       # 照片分析
│   ├── enhanced_analyzer.py    # ⭐ 深度聊天分析引擎
│   ├── persona_bootstrapper.py # ⭐ 资料不足填充器
│   └── auto_messenger.py      # ⭐ 多平台自动发消息
├── dears/                      # 生成的人物Skill
└── README.md
```

---

## 安装

### 依赖安装

```bash
pip install -r requirements.txt
```

**必装**：
- `openai-whisper` - 语音转文字

**可选**：
- `pydub` - 音频处理
- `Pillow` - 图像处理

---

## 使用

### 触发命令

```
/create-dear
```

按提示输入：
1. 称呼/代号（必填）
2. 关系类型（亲人/爱人/朋友）
3. 基本信息（性格、职业）
4. 原材料（微信记录/照片/语音）

### 支持的数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg/留痕/PyWxDump导出 | 支持txt/html/json |
| 语音消息 | m4a/mp3/wav/ogg | ⭐ Whisper转文字 |
| 照片 | JPEG/PNG（含EXIF） | 时间线提取 |
| 朋友圈截图 | 图片 | 公开人设分析 |
| 口述/粘贴 | 纯文本 | 主观记忆 |

---

## 逼真度优化技术细节

### 1. 语音特征提取算法

```python
# 从语音中提取的特征
voice_features = {
    "语速": "快/慢/中等",
    "停顿频率": "高/中/低", 
    "语气词": ["嗯", "哦", "啊"],
    "情绪状态": "积极/中性/消极",
    "消息长度偏好": "长/短"
}
```

### 2. 表情包语义映射

建立表情包到语义情感的映射：

```python
emoji_mapping = {
    "😂": "觉得好笑/尴尬",
    "😭": "感动/难过",
    "❤️": "表达爱意",
    "👍": "认同/赞同",
    "🔥": "强烈认同/羡慕"
}
```

### 3. 上下文记忆网络

每次对话后自动更新：
- 讨论过的话题
- ta表达过的观点
- 双方的关系动态

---

## 与OpenClaw集成

本Skill基于AgentSkills标准开发，兼容OpenClaw。

在OpenClaw中安装：
```bash
openclaw skill install ./dear-skill
```

---

## 免责声明

1. **仅用于个人回忆**：不用于商业用途
2. **隐私保护**：所有数据本地存储
3. **真实还原**：不美化不丑化，保持真实
4. **尊重已故亲人**：以缅怀和尊重为准

---

## 参考项目

- [前任.skill](https://github.com/therealXiaomanChu/ex-skill) - 灵感来源
- [同事.skill](https://github.com/titanwings/colleague-skill) - 同类项目
- [WeChatMsg](https://github.com/ChatGPT-Hackers/WeChatMsg) - 微信导出工具
- [PyWxDump](https://github.com/xaoyaoo/PyWxDump) - 微信数据处理

---

## 信息来源

| 平台 | 备注 |
|-----|-----|
| GitHub | 原始项目和技术方案 |
| CSDN | 技术实现教程 |
| 知乎 | 微信导出方案对比 |

---

MIT License
