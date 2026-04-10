#!/usr/bin/env python3
"""
Auto Messenger - 多平台自动发消息模块
支持：Telegram / 微信(PC) / 钉钉 / 飞书
"""

import os
import json
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from pathlib import Path


class BaseMessenger(ABC):
    """消息发送基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接平台"""
        pass
    
    @abstractmethod
    def send(self, message: str, recipient: str = None) -> bool:
        """发送消息"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """获取连接状态"""
        pass


class TelegramMessenger(BaseMessenger):
    """Telegram Bot 发送器"""
    
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.chat_id = None
        
    def connect(self) -> bool:
        """连接Telegram Bot"""
        if not self.bot_token:
            print("❌ 未配置TELEGRAM_BOT_TOKEN")
            return False
            
        import urllib.request
        url = f"{self.api_url}/getMe"
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read())
                if result.get("ok"):
                    print(f"✅ Telegram Bot已连接: {result['result']['username']}")
                    return True
        except Exception as e:
            print(f"❌ Telegram连接失败: {e}")
        return False
    
    def send(self, message: str, chat_id: str = None) -> bool:
        """发送消息"""
        target_id = chat_id or self.chat_id
        if not target_id:
            print("❌ 未指定发送目标")
            return False
            
        import urllib.request
        import urllib.parse
        
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": target_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            req = urllib.request.Request(
                url, 
                data=urllib.parse.urlencode(data).encode()
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                return result.get("ok", False)
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def set_chat_id(self, chat_id: str):
        """设置默认聊天ID"""
        self.chat_id = chat_id
    
    def get_status(self) -> Dict:
        return {
            "platform": "telegram",
            "connected": bool(self.bot_token),
            "has_token": bool(self.bot_token)
        }


class WeChatPCMessenger(BaseMessenger):
    """微信PC端自动化发送器（需配合PC客户端）"""
    
    def __init__(self):
        self.enabled = False
        self.wx_id = None
        
    def connect(self) -> bool:
        """检测微信PC客户端"""
        try:
            # 检测是否安装了微信PC版
            import subprocess
            result = subprocess.run(
                ["tasklist"], 
                capture_output=True, 
                text=True
            )
            if "WeChat.exe" in result.stdout:
                print("✅ 检测到微信PC客户端")
                self.enabled = True
                return True
            else:
                print("⚠️ 未检测到微信PC客户端，请先打开微信")
                return False
        except Exception as e:
            print(f"❌ 检测失败: {e}")
        return False
    
    def send(self, message: str, contact_name: str = None) -> bool:
        """
        发送消息（通过Windows UI自动化）
        注意：此功能有封号风险，建议仅用于测试
        """
        if not self.enabled:
            print("❌ 微信未连接")
            return False
            
        try:
            import pyautogui
            import pywinauto
            
            # 激活微信窗口
            # ... 复杂实现
            
            return True
        except ImportError:
            print("❌ 需要安装pyautogui: pip install pyautogui")
            return False
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        return {
            "platform": "wechat_pc",
            "enabled": self.enabled,
            "warning": "微信PC端自动化有封号风险"
        }


class DingTalkMessenger(BaseMessenger):
    """钉钉Webhook发送器"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("DINGTALK_WEBHOOK")
        
    def connect(self) -> bool:
        """测试钉钉Webhook"""
        if not self.webhook_url:
            print("❌ 未配置DINGTALK_WEBHOOK")
            return False
        return True
    
    def send(self, message: str, at_mobiles: List[str] = None) -> bool:
        """通过Webhook发送消息"""
        import urllib.request
        
        data = {
            "msgtype": "text",
            "text": {"content": message}
        }
        
        if at_mobiles:
            data["at"] = {"atMobiles": at_mobiles}
            
        try:
            req = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                return result.get("errcode") == 0
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        return {
            "platform": "dingtalk",
            "connected": bool(self.webhook_url)
        }


class FeishuMessenger(BaseMessenger):
    """飞书Webhook发送器"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("FEISHU_WEBHOOK")
        
    def connect(self) -> bool:
        if not self.webhook_url:
            print("❌ 未配置FEISHU_WEBHOOK")
            return False
        return True
    
    def send(self, message: str) -> bool:
        """通过Webhook发送消息"""
        import urllib.request
        
        data = {
            "msg_type": "text",
            "content": {"text": message}
        }
        
        try:
            req = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                return result.get("code") == 0 or result.get("StatusCode") == 0
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        return {
            "platform": "feishu",
            "connected": bool(self.webhook_url)
        }


class AutoMessenger:
    """
    自动发消息引擎
    分析聊天习惯，自动定时发送消息
    """
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.messengers: Dict[str, BaseMessenger] = {
            "telegram": TelegramMessenger(),
            "wechat": WeChatPCMessenger(),
            "dingtalk": DingTalkMessenger(),
            "feishu": FeishuMessenger(),
        }
        self.current_platform = None
        
    def _load_config(self, path: str = None) -> Dict:
        """加载配置"""
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_config(self, path: str = None):
        """保存配置"""
        config_path = path or "auto_messenger_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
            
    def setup_platform(self, platform: str, **kwargs) -> bool:
        """
        设置发送平台
        
        Args:
            platform: telegram / wechat / dingtalk / feishu
            **kwargs: 平台特定参数
        """
        if platform not in self.messengers:
            print(f"❌ 不支持的平台: {platform}")
            return False
            
        messenger = self.messengers[platform]
        
        if platform == "telegram":
            token = kwargs.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN")
            if token:
                messenger = TelegramMessenger(token)
                self.messengers["telegram"] = messenger
                
        elif platform == "dingtalk":
            webhook = kwargs.get("webhook_url") or os.getenv("DINGTALK_WEBHOOK")
            if webhook:
                messenger = DingTalkMessenger(webhook)
                self.messengers["dingtalk"] = messenger
                
        elif platform == "feishu":
            webhook = kwargs.get("webhook_url") or os.getenv("FEISHU_WEBHOOK")
            if webhook:
                messenger = FeishuMessenger(webhook)
                self.messengers["feishu"] = messenger
        
        # 测试连接
        success = messenger.connect()
        if success:
            self.current_platform = platform
            self.config["platform"] = platform
            self._save_config()
            print(f"✅ 已切换到 {platform}")
        else:
            print(f"❌ {platform} 连接失败")
            
        return success
    
    def learn_sending_habits(self, messages: List[Dict]) -> Dict:
        """
        从聊天记录学习发送习惯
        
        Args:
            messages: [{"timestamp": "...", "sender": "ta", "content": "..."}]
        """
        if not messages:
            return {}
            
        # 分析发送时间段
        hours = []
        for msg in messages:
            try:
                ts = msg.get("timestamp", "")
                if ts:
                    hour = datetime.fromisoformat(ts).hour
                    hours.append(hour)
            except:
                pass
                
        # 统计高频发送时段
        from collections import Counter
        hour_counts = Counter(hours)
        peak_hours = [h for h, _ in hour_counts.most_common(3)]
        
        # 分析发送频率
        if len(messages) >= 2:
            try:
                t1 = datetime.fromisoformat(messages[0].get("timestamp", ""))
                t2 = datetime.fromisoformat(messages[-1].get("timestamp", ""))
                days = (t2 - t1).days or 1
                daily_avg = len(messages) / days
            except:
                daily_avg = 1
        else:
            daily_avg = 1
            
        habits = {
            "peak_hours": peak_hours,
            "daily_avg_messages": round(daily_avg, 2),
            "total_messages": len(messages),
            "recommended_send_times": self._recommend_send_times(peak_hours),
        }
        
        self.config["habits"] = habits
        self._save_config()
        
        return habits
    
    def _recommend_send_times(self, peak_hours: List[int]) -> List[str]:
        """基于活跃时段推荐发送时间"""
        if not peak_hours:
            return ["09:00", "12:00", "21:00"]
            
        recommendations = []
        for hour in peak_hours[:2]:
            if hour < 12:
                recommendations.append(f"{hour}:00 (上午)")
            elif hour < 18:
                recommendations.append(f"{hour}:00 (下午)")
            else:
                recommendations.append(f"{hour}:00 (晚上)")
                
        return recommendations
    
    def generate_auto_message(self, persona: Dict, context: str = None) -> str:
        """
        生成符合角色风格的消息
        
        Args:
            persona: 角色Persona信息
            context: 上下文（节日/生日/日常）
        """
        habits = self.config.get("habits", {})
        layer2 = persona.get("layer2_speaking_style", {})
        
        # 根据context生成不同类型消息
        if context == "birthday":
            templates = [
                "生日快乐呀🎂，今年有什么想实现的愿望吗？",
                "又长大一岁啦，时间过得好快...",
            ]
        elif context == "festival":
            templates = [
                "{name}，节日快乐🎉",
                "今天{day}，记得好好休息~",
            ]
        else:
            # 日常关心
            layer3 = persona.get("layer3_emotional", {})
            love_expr = layer3.get("love_expression", "")
            
            if "注意" in love_expr or "身体" in love_expr:
                templates = [
                    "最近怎么样？不要太累了",
                    "记得按时吃饭呀",
                ]
            else:
                templates = [
                    "在干嘛呢？",
                    "最近怎么样？",
                ]
                
        import random
        message = random.choice(templates)
        
        # 替换占位符
        name = persona.get("layer1_identity", {}).get("relation", "你")
        message = message.replace("{name}", name)
        
        return message
    
    def send_auto(self, persona: Dict, context: str = None) -> bool:
        """自动发送消息"""
        if not self.current_platform:
            print("❌ 未选择发送平台")
            return False
            
        messenger = self.messengers.get(self.current_platform)
        if not messenger:
            return False
            
        message = self.generate_auto_message(persona, context)
        return messenger.send(message)
    
    def enable_scheduled_send(self, persona: Dict, interval_hours: int = 24):
        """
        启用定时发送
        
        Args:
            interval_hours: 发送间隔（小时）
        """
        self.config["scheduled"] = {
            "enabled": True,
            "interval_hours": interval_hours,
            "last_send": None,
            "persona_summary": {
                "relation": persona.get("layer1_identity", {}).get("relation"),
                "name": persona.get("layer0_hard_rules", "").split("\n")[1] if persona.get("layer0_hard_rules") else ""
            }
        }
        self._save_config()
        print(f"✅ 已启用定时发送，每 {interval_hours} 小时发送一次")
        
    def check_and_send(self, persona: Dict) -> bool:
        """检查是否应该发送"""
        scheduled = self.config.get("scheduled", {})
        if not scheduled.get("enabled"):
            return False
            
        last_send = scheduled.get("last_send")
        interval = scheduled.get("interval_hours", 24)
        
        should_send = False
        if not last_send:
            should_send = True
        else:
            try:
                last = datetime.fromisoformat(last_send)
                if (datetime.now() - last).total_seconds() >= interval * 3600:
                    should_send = True
            except:
                should_send = True
                
        if should_send:
            success = self.send_auto(persona)
            if success:
                self.config["scheduled"]["last_send"] = datetime.now().isoformat()
                self._save_config()
            return success
            
        return False
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "current_platform": self.current_platform,
            "platforms": {
                name: messenger.get_status() 
                for name, messenger in self.messengers.items()
            },
            "scheduled": self.config.get("scheduled", {}),
            "habits": self.config.get("habits", {})
        }


def main():
    """测试"""
    auto = AutoMessenger()
    
    # 显示可用平台
    print("=== 自动发消息模块 ===")
    print("支持的平台:")
    for name in auto.messengers.keys():
        print(f"  - {name}")
    
    print("\n状态:")
    status = auto.get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
