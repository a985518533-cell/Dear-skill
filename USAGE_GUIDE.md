# 亲人/爱人.skill 使用指南

> 从零开始，完整教程

---

## 目录

1. [环境准备](#1-环境准备)
2. [安装依赖](#2-安装依赖)
3. [配置AI模型](#3-配置ai模型)
4. [安装技能](#4-安装技能)
5. [创建第一个亲人Skill](#5-创建第一个亲人skill)
6. [导入聊天记录](#6-导入聊天记录)
7. [对话与训练](#7-对话与训练)
8. [自动发消息配置](#8-自动发消息配置)
9. [常见问题](#9-常见问题)

---

## 1. 环境准备

### 系统要求

| 项目 | 要求 |
|-----|-----|
| 操作系统 | Windows 10/11, macOS, Linux |
| Python | 3.9 或更高 |
| 内存 | 推荐 8GB+ |
| 存储 | 2GB+ 可用空间 |

### 安装Python

**Windows：**

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.9 或更高版本
3. 运行安装程序
4. **⚠️ 重要：勾选 "Add Python to PATH"**

**macOS：**

```bash
# 使用Homebrew安装
brew install python3
```

**验证安装：**

```bash
python --version
# 应该显示 Python 3.9.x 或更高
```

---

## 2. 安装依赖

### 克隆项目

```bash
git clone https://github.com/a985518533-cell/Dear-skill.git
cd Dear-skill
```

### 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 安装Python依赖

```bash
pip install -r requirements.txt
```

### 必装依赖说明

| 依赖 | 用途 | 是否必装 |
|-----|-----|---------|
| openai-whisper | 语音转文字 | ✅ 必装 |
| pydub | 音频处理 | 可选 |
| Pillow | 图像处理 | 可选 |
| requests | HTTP请求 | 可选 |

### 安装Whisper（语音转文字）

```bash
# 安装Whisper
pip install openai-whisper

# 或使用PyTorch版本（更快）
pip install torch torchvision
pip install openai-whisper
```

### 安装FFmpeg（音频处理必需）

**Windows：**

1. 下载 https://www.gyan.dev/ffmpeg/builds/
2. 选择 `ffmpeg-release-essentials.zip`
3. 解压到 `C:\ffmpeg`
4. 将 `C:\ffmpeg\bin` 添加到系统PATH

**macOS：**

```bash
brew install ffmpeg
```

**Linux：**

```bash
sudo apt update
sudo apt install ffmpeg
```

**验证安装：**

```bash
ffmpeg -version
```

---

## 3. 配置AI模型

### 支持的模型

| 模型 | 提供商 | 特点 | 推荐场景 |
|-----|-------|-----|---------|
| **DeepSeek** | deepseek-chat | 便宜、快速 | 日常对话 |
| **MinMax** | MiniMax-M2 | 中文优化 | 中文对话 |
| **GPT-4o Mini** | OpenAI | 效果好 | 追求质量 |

### 配置DeepSeek（推荐）

1. 获取API Key：
   - 访问 https://platform.deepseek.com/
   - 注册账号并获取API Key

2. 配置环境变量：
   ```bash
   # Windows
   setx DEEPSEEK_API_KEY "your-api-key-here"
   
   # macOS/Linux
   export DEEPSEEK_API_KEY="your-api-key-here"
   ```

### 配置MinMax

1. 获取API Key（从MinMax平台）
2. 配置：
   ```bash
   export MINMAX_API_KEY="your-api-key-here"
   ```

### 配置OpenAI（可选）

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 在OpenClaw中配置模型

```bash
# 打开配置
openclaw config edit

# 添加模型配置示例
models:
  - name: deepseek
    provider: deepseek
    model: deepseek-chat
    api_key: ${DEEPSEEK_API_KEY}
    
  - name: MinMax
    provider: minmax
    model: MiniMax-M2
    api_key: ${MINMAX_API_KEY}
```

---

## 4. 安装技能

### 方式一：通过OpenClaw安装

```bash
# 安装本地Skill
openclaw skill install ./Dear-skill

# 或从GitHub安装
openclaw skill install https://github.com/a985518533-cell/Dear-skill
```

### 方式二：复制到Skills目录

```bash
# 找到OpenClaw的skills目录
# Windows通常在：
# C:\Users\你的用户名\.openclaw\workspace\skills

# 复制Dear-skill文件夹到skills目录
```

### 验证安装

```bash
openclaw skill list
# 应该看到 dear-skill 或 create-dear
```

---

## 5. 创建第一个亲人Skill

### 启动创建

在OpenClaw中输入：

```
/create-dear
```

或直接说：

```
帮我创建一个亲人的skill
我想蒸馏我的妈妈
给我做一个XX的skill
```

### Step 1：回答4个问题

```
=== 亲人/爱人.skill 创建器 ===

请提供以下信息：

1️⃣ 称呼/代号是什么？
   （示例：妈妈、爸爸、老婆、外婆）

   → 输入：妈妈

2️⃣ 和你是什么关系？
   选项：
   [1] 亲人（父母/祖辈/兄弟姐妹）
   [2] 爱人（情侣/夫妻）
   [3] 朋友（闺蜜/挚友）

   → 输入：1

3️⃣ 用一句话介绍ta：
   （职业、性格、你们的关系）
   
   示例：退休教师，操心命，每天都要问我吃了没
   
   → 输入：你的回答

4️⃣ 特殊说明？
   - ta是否已故？（影响语气）
   - 有什么方言/口音？
   - 其他需要保留的特点？
   
   → 输入：你的回答（可以跳过）
```

### Step 2：选择数据导入方式

```
你有以下原材料可以导入：

[1] 微信聊天记录导出
    支持：WeChatMsg、留痕、PyWxDump导出的txt/html/json
    
[2] 照片（带EXIF信息）
    会提取：拍摄时间、地点、时间线
    
[3] 语音消息
    用Whisper转文字，保留原声特征描述
    
[4] 手写日记/备忘录
    扫描或拍照上传
    
[5] 直接粘贴/口述
    把你记得的事情告诉我
    
[6] 跳过（仅凭手动信息生成）

请输入数字，可以多选（如：1,3,5）：
```

### Step 3：等待AI分析

```
⏳ AI正在分析你的原材料...

✅ 完成分析：
- 提取了 1,234 条聊天记录
- 识别了 15 个常用口头禅
- 分析了发送习惯（活跃时间：晚上8-10点）
- 提取了关系记忆：23 条

🎯 逼真度预估：78%
（聊天记录量足够，但建议补充照片）
```

### Step 4：预览确认

```
=== 预览 ===

称呼：妈妈
关系：亲人
性格：操心命、话多、温柔
口头禅："记得吃饭"、"别熬夜"、"在外面要照顾好自己"

生成的关系记忆：
• 每次回家都会准备一桌子菜
• 经常担心我在外面吃不好
• 会在家庭群发养生文章
• ...

生成的性格特征：
• 说话风格：关心型，常用"别/要/记得"
• 消息长度：中等偏短
• 情绪表达：温暖、直接
• ...

确认生成？
[y/N]
```

### Step 5：完成

```
🎉 亲人Skill创建成功！

保存位置：./dears/ma_ma/

对话入口：/ma_ma 或 直接说"和妈妈聊天"

下一步建议：
1. 先测试对话，看语气是否正确
2. 如有偏差，用"ta不会这样说"纠正
3. 开启自动发消息功能
```

---

## 6. 导入聊天记录

### 6.1 微信聊天记录导出

#### 方式一：WeChatMsg（推荐）

1. 下载地址：https://github.com/ChatGPT-Hackers/WeChatMsg
2. 按照文档导出聊天记录
3. 选择格式：JSON 或 TXT

#### 方式二：留痕

1. 微信搜索"留痕"小程序
2. 导出聊天记录
3. 选择JSON格式

#### 方式三：PyWxDump

1. 安装：`pip install PyWxDump`
2. 使用文档：https://github.com/xaoyaoo/PyWxDump

### 6.2 导入命令

```bash
# 方式一：直接在技能中指定文件路径
/create-dear
# 然后在对话中提供文件路径

# 方式二：使用工具解析后导入
python tools/wechat_parser.py \
  --file 你导出的聊天记录.json \
  --target 妈妈 \
  --output parsed_chats.json
```

### 6.3 语音消息处理

```bash
# 将语音文件夹转换为文字
python tools/voice_parser.py \
  --input ./voice_messages/ \
  --output voice_text.txt \
  --batch \
  --model base
```

参数说明：
| 参数 | 说明 | 默认值 |
|-----|-----|-------|
| `--input` | 语音文件/文件夹路径 | 必填 |
| `--output` | 输出文本文件路径 | 必填 |
| `--model` | Whisper模型 | base |
| `--language` | 语言 | zh |
| `--batch` | 批量处理文件夹 | false |

Whisper模型选择：
| 模型 | 速度 | 精度 | 内存需求 |
|-----|-----|-----|---------|
| tiny | 最快 | 较低 | ~1GB |
| base | 快 | 中等 | ~1GB |
| small | 较慢 | 较高 | ~2GB |
| medium | 慢 | 高 | ~5GB |

### 6.4 照片导入

```bash
# 分析照片，提取时间线和地点
python tools/photo_analyzer.py \
  --input ./photos/ \
  --output photo_analysis.json
```

---

## 7. 对话与训练

### 7.1 基础对话

创建完成后，通过以下方式对话：

```
# 方式一：命令触发
/ma_ma

# 方式二：直接说
和妈妈聊天
问问妈妈最近怎么样
```

### 7.2 纠正训练

当AI说的不像时，纠正它：

```
# 纠正格式
ta不会这样说，应该是...

# 或者
不对，ta会说...
```

AI会自动学习并更新Persona。

### 7.3 追加记忆

```
我想起来了，之前...

再补充一点...

我找到了更多聊天记录
```

### 7.4 查看状态

```
# 查看当前亲人Skill的状态
/ma_ma-status

# 或
查看妈妈的信息
```

---

## 8. 自动发消息配置

### 8.1 开启自动发送

```
/auto-send
```

### 8.2 选择平台

```
=== 自动发消息平台选择 ===

请选择发送平台：

[1] Telegram Bot ✅（推荐，稳定）
    需要配置 Bot Token
    
[2] 钉钉 Webhook
    需要配置 Webhook URL
    
[3] 飞书 Webhook
    需要配置 Webhook URL
    
[4] 微信 PC 端 ⚠️（有封号风险）
    需要保持微信PC客户端运行

请输入数字 [1-4]：
```

### 8.3 Telegram配置

1. 在Telegram中找 @BotFather
2. 发送 `/newbot`
3. 给机器人起名字
4. 获取Bot Token
5. 告诉机器人你的Chat ID（找 @userinfobot）

配置示例：
```
请提供 Telegram Bot Token：
 BotFather给你的token

请提供你的 Chat ID：
 找@userinfobot获取
```

### 8.4 钉钉/飞书配置

1. 在群设置中添加"自定义机器人"
2. 复制Webhook URL

配置示例：
```
请提供 Webhook URL：
 https://oapi.dingtalk.com/robot/send?access_token=xxx
```

### 8.5 微信PC端（风险警告）

```
⚠️ 警告：微信PC端自动化有封号风险
确认开启？
[y/N]
```

**注意：** 不建议频繁使用，有封号风险。

### 8.6 设置发送频率

```
=== 发送频率设置 ===

当前分析到的发送习惯：
- 活跃时间：晚上 20:00-22:00
- 平均每天发送 3-5 条
- 话题类型：关心吃饭、提醒休息

选择发送频率：
[1] 每天1次（推荐）
[2] 每天2次
[3] 每周3次
[4] 自定义

发送时间建议：20:00（晚上8点）

确认开启？[y/N]
```

### 8.7 查看/关闭

```
# 查看自动发送状态
/auto-send-status

# 关闭自动发送
/auto-send-off
```

---

## 9. 常见问题

### Q1: 提示"找不到Python"或"Python版本不对"

**解决：**
```bash
# 检查Python是否安装
python --version

# 如果没安装，参考第一章安装Python

# 如果安装但版本不对，下载新版本
```

### Q2: Whisper安装失败

**解决：**
```bash
# 使用管理员权限安装
pip install openai-whisper --user

# 或先安装PyTorch
pip install torch
pip install openai-whisper
```

### Q3: ffmpeg找不到

**解决：**
1. 确认ffmpeg安装成功
2. 确认ffmpeg/bin添加到系统PATH
3. 重启终端/电脑

### Q4: 聊天记录导入失败

**检查：**
1. 文件格式是否正确（JSON/TXT/HTML）
2. 文件编码是否为UTF-8
3. 文件是否损坏

**尝试：**
```bash
# 先用工具解析
python tools/wechat_parser.py --file 你的文件.txt --target 称呼 --output test.json
```

### Q5: AI说的不像怎么办

**解决：**
1. 使用纠正功能：`ta不会这样说...`
2. 追加更多聊天记录
3. 手动调整Persona文件

### Q6: 微信PC端自动发送被封号

**警告：** 微信官方禁止第三方自动化，有封号风险。

**建议：**
- 使用Telegram替代
- 或仅做测试用途

### Q7: 如何更新Persona

```bash
# 追加新的聊天记录
/ma_ma 追加记忆

# 重新训练
/ma_ma 更新
```

### Q8: 模型选择建议

| 场景 | 推荐模型 |
|-----|---------|
| 日常测试 | DeepSeek（便宜） |
| 中文对话为主 | MinMax |
| 追求效果 | GPT-4o Mini |

---

## 附录

### 目录结构

```
Dear-skill/
├── SKILL.md                    # 技能入口
├── README.md                   # 项目说明
├── USAGE_GUIDE.md             # 本文档
├── requirements.txt           # 依赖
├── prompts/                    # Prompt模板
│   ├── intake.md              # 信息录入
│   ├── memory_builder.md      # 记忆生成
│   └── persona_builder.md     # 性格生成
├── tools/                      # 工具
│   ├── voice_parser.py        # 语音解析
│   ├── wechat_parser.py       # 微信解析
│   ├── enhanced_analyzer.py    # 深度分析
│   ├── auto_messenger.py      # 自动发送
│   └── photo_analyzer.py       # 照片分析
└── dears/                      # 生成的Skill（运行时创建）
    └── {slug}/
        ├── memory.md
        ├── persona.md
        └── SKILL.md
```

### 相关链接

| 资源 | 地址 |
|-----|-----|
| GitHub | https://github.com/a985518533-cell/Dear-skill |
| WeChatMsg | https://github.com/ChatGPT-Hackers/WeChatMsg |
| PyWxDump | https://github.com/xaoyaoo/PyWxDump |
| Whisper | https://github.com/openai/whisper |

---

*祝您使用愉快！*
