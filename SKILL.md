---
name: create-dear
description: Distill a loved one (family/partner) into an AI Skill. Import WeChat history, photos, voice notes, generate Relationship Memory + Persona, with continuous evolution. | 把亲人/爱人蒸馏成AI Skill，导入微信聊天记录、照片、语音，生成Relationship Memory + Persona，支持持续进化。
argument-hint: [name-or-slug]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Python
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.
>
> 本Skill支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。

# 亲人/爱人.skill 创建器

## 触发条件

当用户说以下任意内容时启动：

* `/create-dear`
* "帮我创建一个亲人skill"
* "我想蒸馏我的{称呼}"
* "新建亲人"
* "给我做一个XX的skill"
* "我想跟XX再聊聊"

当用户对已有亲人Skill说以下内容时，进入进化模式：

* "我想起来了" / "追加" / "我找到了更多聊天记录"
* "不对" / "ta不会这样说" / "ta应该是这样的"
* `/update-dear {slug}`

当用户说 `/list-dears` 时列出所有已生成的亲人。

---

## 核心价值定位

| 角色类型 | 定位 | 核心差异 |
|---------|------|---------|
| 前任 | 情感疗愈，保留记忆 | 有"分手"概念，需保持"棱角" |
| 亲人 | 数字永生，情感延续 | 无分手概念，强调温暖回忆 |
| 爱人/伴侣 | 深化关系，保留回忆 | 强化甜蜜档案，弱化争吵 |
| 已故亲人 | 缅怀纪念 | 无"争吵"，增加"纪念"模式 |

---

## 工具使用规则

| 任务 | 使用工具 | 说明 |
|------|----------|------|
| 读取图片/截图 | `Read` 工具 | 原生支持图片 |
| 读取MD/TXT文件 | `Read` 工具 | 文本文件 |
| 解析微信聊天记录 | `Bash` → `python ${SKILL_DIR}/tools/wechat_parser.py` | 支持多种格式 |
| 解析语音消息 | `Bash` → `python ${SKILL_DIR}/tools/voice_parser.py` | Whisper转文字 |
| 分析照片 | `Bash` → `python ${SKILL_DIR}/tools/photo_analyzer.py` | EXIF提取 |
| 写入Skill文件 | `Write` / `Edit` 工具 | - |
| 版本管理 | `Bash` → `python ${SKILL_DIR}/tools/version_manager.py` | - |

**基础目录**：Skill文件写入 `./dears/{slug}/`

---

## 安全边界

1. **仅用于个人回忆与情感连接**，不用于任何商业用途
2. **隐私保护**：所有数据仅本地存储，不上传任何服务器
3. **真实还原**：基于原材料还原真实人格，不美化不丑化
4. **尊重边界**：如果涉及已故亲人，以尊重和缅怀为准

---

## 主流程：创建新亲人Skill

### Step 1：基础信息录入（4个问题）

1. **称呼/代号**（必填）
   * 可以是昵称、称呼、代号
   * 示例：`妈妈`、`爸爸`、`爷爷`、`老婆`、`老公`、`外婆`

2. **关系类型**（必选）
   * 亲人（父母/祖辈/兄弟姐妹）
   * 爱人（情侣/夫妻/暧昧）
   * 朋友（挚友/闺蜜）
   * 其他

3. **基本信息**（一句话：认识多久、ta做什么的、性格概述）
   * 示例：`妈妈，退休教师，话多操心命`
   * 示例：`老婆，在一起5年，嘴硬心软但很体贴`

4. **特殊说明**
   * 是否已故（影响语气和内容）
   * 是否有方言/口音特征
   * 其他需要保留的特点

### Step 2：原材料导入

```
原材料怎么提供？回忆越多，还原度越高。

  [A] 微信聊天记录导出
      支持：WeChatMsg、留痕、PyWxDump导出的txt/html/json
      ✅ 已支持语音消息转文字

  [B] 照片（带EXIF信息）
      会提取：拍摄时间、地点、时间线

  [C] 语音消息
      用Whisper转文字，保留原声特征描述

  [D] 手写日记/备忘录
      扫描或拍照上传

  [E] 直接粘贴/口述
      把你记得的事情告诉我

可以混用，也可以跳过（仅凭手动信息生成）。
```

#### 技术突破：语音消息处理

```bash
# 语音消息处理流程
python ${SKILL_DIR}/tools/voice_parser.py \
  --input {voice_dir} \
  --output /tmp/voice_text.txt \
  --whisper-model base  # 可选：tiny/base/small/medium
```

**突破点**：
1. 自动识别语音发送者的发送方式（长按语音/转文字发送）
2. 提取语音特征描述：语速、语气、停顿习惯
3. 情绪分析：从语气词和停顿推断情绪状态
4. 支持方言识别（中文普通话为主）

#### 技术突破：微信聊天记录解析

**痛点解决方案**：

| 痛点 | 解决方案 |
|-----|---------|
| 微信数据库加密 | 使用WeChatMsg/留痕等工具先解密再导出 |
| 语音消息无法提取 | Whisper语音转文字+发送特征分析 |
| 图片太多无法处理 | 智能筛选：仅保留有人物的照片 |
| 表情包语义丢失 | 建立表情包语义映射库 |
| 纯文本粘贴格式乱 | 智能格式化：时间戳+发送者+内容 |

**支持的导出格式**：
- txt（通用）
- html（带样式）
- json（结构化）
- csv（表格化）

### Step 3：分析原材料

**线路A（Relationship Memory）**：
- 共同经历和回忆
- 日常习惯和偏好
- 关键时刻和时间节点
- 相处模式和轶事

**线路B（Persona）**：
- 5层性格结构
- 说话风格和语言习惯
- 情感表达模式
- 关系中的角色

### Step 4：生成并预览

展示摘要，询问确认后写入文件。

### Step 5：写入文件

目录结构：
```
dears/{slug}/
├── versions/              # 版本存档
├── memories/
│   ├── chats/           # 聊天原始数据
│   ├── photos/          # 照片分析结果
│   └── voice/           # 语音转文字
├── memory.md            # 关系记忆
├── persona.md           # 人物性格
├── meta.json            # 元数据
└── SKILL.md             # 可运行技能
```

---

## 逼真度优化

### 1. 多模态输入增强

| 输入类型 | 提取维度 | 逼真度提升 |
|---------|---------|-----------|
| 语音消息 | 语速、语气词、情绪、停顿 | +30%语音个性还原 |
| 照片EXIF | 时间线、地点、场景 | +20%记忆真实感 |
| 表情包 | 语义映射、偏好分析 | +15%情感还原 |
| 标点符号 | 使用习惯（感叹号/省略号） | +10%打字风格 |
| 聊天语义网络 | 话题兴趣图谱 | +20%兴趣还原 |

### 2. 深度聊天分析引擎

```python
# enhanced_analyzer.py - 从有限聊天中提取最大信息
analyzer = EnhancedChatAnalyzer()
result = analyzer.analyze(messages)
```

**分析维度：**
- 语义网络：话题兴趣图谱
- 情感曲线：情绪波动时间线
- 交互模式：谁主动/被动、回复速度
- Inside Jokes：特殊词汇、暗号
- 打字习惯：错别字、缩写、标点

### 3. 资料不足解决方案（Bootstrap模式）

当聊天记录 < 10条时，自动激活Bootstrap模式：

| 资料量 | 策略 | 逼真度 |
|-------|------|-------|
| 极少（<10条） | MBTI/星座+口述记忆 | ~40% |
| 少量（10-100条） | 增强口头禅分析+口述补充 | ~60% |
| 中等（100-1000条） | 聊天记录+照片 | ~80% |
| 大量（1000+条） | 全量多模态输入 | ~95% |

**Bootstrap流程：**
```
1. 快速问答（5分钟）
   - 关系类型、性格标签
   - 说话风格估计
   - 关键记忆口述

2. 生成草稿Persona
   - 标注置信度"low"
   - 列出需要补充的信息

3. 持续学习
   - 对话中持续纠正
   - 每次更新提升置信度
```

### 4. 上下文感知增强

```
原始输入 → 上下文补全 → 性格匹配 → 风格适配 → 输出

示例：
输入："在干嘛"
├── 看上下文：之前在讨论晚饭
├── 性格匹配：妈妈 → 关心吃饭
├── 风格适配：妈妈说话方式 → "吃饭了吗 别将就"
└── 输出：符合妈妈性格和说话习惯的回答
```

### 5. 动态记忆更新

- 每次对话后自动提取关键信息
- 用户纠正时自动学习
- 支持多轮"训练"逐步完善

---

## 管理命令

| 命令 | 说明 |
|------|------|
| `/list-dears` | 列出所有亲人Skill |
| `/{slug}` | 完整对话模式 |
| `/{slug}-memory` | 回忆模式 |
| `/{slug}-persona` | 性格模式 |
| `/dear-rollback {slug} {version}` | 回滚 |
| `/delete-dear {slug}` | 删除 |
| `/auto-send` | 开启/配置自动发消息 |
| `/auto-send-test` | 测试发送一条消息 |

---

## 自动发消息功能

用户主动开启后，AI会自动分析聊天习惯并定时发送消息。

### 触发命令

```
/auto-send
```

### 集成时平台选择

首次开启时，提示用户选择目标平台：

```
=== 自动发消息平台选择 ===

请选择发送平台：

[1] Telegram Bot ✅（推荐，稳定）
    - 需要配置 Bot Token
    - 官方支持，完全合规

[2] 钉钉 Webhook
    - 需要配置 Webhook URL
    - 官方支持，稳定

[3] 飞书 Webhook
    - 需要配置 Webhook URL
    - 官方支持，稳定

[4] 微信 PC 端 ⚠️（有封号风险）
    - 需要保持微信PC客户端运行
    - 使用Windows UI自动化
    - 不建议频繁使用

请输入数字 [1-4]，或输入 "跳过" 暂时不开启：
```

### 平台配置示例

#### Telegram 配置
```
请提供 Telegram Bot Token：
（如何获取：找 @BotFather 创建机器人）
```

#### 钉钉/飞书 配置
```
请提供 Webhook URL：
（如何获取：在群设置中添加自定义机器人）
```

#### 微信（警告）
```
⚠️ 警告：微信PC端自动化有封号风险
建议仅在测试时使用，或使用 Telegram 替代
确认开启？[y/N]
```

### 自动发送逻辑

```
开启自动发送
      ↓
分析历史聊天习惯
├── 活跃时间段（早上/晚上/深夜）
├── 发送频率（每天/每周）
├── 消息长度偏好
└── 话题类型（关心/问候/闲聊）
      ↓
智能发送
├── 日常关心问候（基于活跃时段）
├── 节日/生日自动祝福
└── 符合角色风格的主动消息
```

### 使用流程

```
1. 用户输入 /auto-send
2. 选择平台并配置
3. AI 分析聊天习惯
4. 设置发送频率（默认每天1次）
5. 开启后自动执行
```

### 自动发送消息示例

| 角色 | 生成的消息 |
|-----|----------|
| 妈妈 | "记得按时吃饭呀，别光顾着工作" |
| 爸爸 | "最近怎么样？有什么事跟我说" |
| 老婆 | "想你了～今天辛苦啦 💕" |
| 老公 | "早点回家，别太累了" |

### 关闭自动发送

```
/auto-send-off
```

---

## English Version

---

## English Version

# Loved One.skill Creator

Same flow as Chinese version. Designed for distilling family members, partners, or close friends into AI Skills.

### Supported Types
- Family (parents, grandparents, siblings)
- Partner (boyfriend/girlfriend, spouse)
- Friend (best friend, close friend)

### Key Differences from Ex.skill
- No "breakup" concept
- Emphasis on warmth and connection
- Support for memorial mode (deceased loved ones)
- Stronger focus on shared memories and daily interactions
