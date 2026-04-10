#!/usr/bin/env python3
"""
Voice Message Parser - 语音消息解析器
使用Whisper将语音转为文字，并提取说话特征
"""

import argparse
import os
import json
from pathlib import Path
from typing import Dict, List

def check_dependencies():
    """检查依赖"""
    errors = []
    
    try:
        import whisper
    except ImportError:
        errors.append("openai-whisper")
        
    return errors


class VoiceParser:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        
    def load_model(self):
        """加载Whisper模型"""
        import whisper
        print(f"加载Whisper {self.model_size} 模型...")
        self.model = whisper.load_model(self.model_size)
        print("模型加载完成")
        
    def extract_audio_features(self, audio_path: str) -> Dict:
        """从音频中提取基本特征（使用ffprobe）"""
        import subprocess
        import re
        
        features = {
            "duration_seconds": 0,
            "has_audio": True,
        }
        
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", 
                 "format=duration,bit_rate", "-of", "json", audio_path],
                capture_output=True, text=True, encoding='utf-8'
            )
            data = json.loads(result.stdout)
            features["duration_seconds"] = float(data.get("format", {}).get("duration", 0))
        except Exception as e:
            features["has_audio"] = False
            
        return features
        
    def transcribe(self, audio_path: str, language: str = "zh") -> Dict:
        """使用Whisper转录音频"""
        if self.model is None:
            self.load_model()
            
        # 转录
        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            verbose=False
        )
        
        # 提取音频特征
        features = self.extract_audio_features(audio_path)
        
        # 分析语速（基于文字和时长）
        text = result["text"].strip()
        duration = features.get("duration_seconds", 1)
        char_count = len(text)
        chars_per_second = char_count / duration if duration > 0 else 0
        
        # 语气词分析
        particles = ["嗯", "哦", "啊", "哈", "呀", "嘛", "呢", "吧", "的", "了"]
        particle_count = sum(text.count(p) for p in particles)
        
        return {
            "text": text,
            "language": language,
            "duration": round(duration, 2),
            "char_count": char_count,
            "chars_per_second": round(chars_per_second, 2),
            "particle_count": particle_count,
            "features": features,
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"]
                }
                for seg in result.get("segments", [])
            ]
        }
    
    def process_batch(self, voice_dir: str, output_path: str, 
                      file_patterns: List[str] = None) -> Dict:
        """批量处理语音文件"""
        if file_patterns is None:
            file_patterns = ["*.m4a", "*.mp3", "*.wav", "*.ogg", "*.amr", "*.silk"]
            
        voice_dir_path = Path(voice_dir)
        results = []
        
        for pattern in file_patterns:
            for file_path in voice_dir_path.glob(pattern):
                print(f"处理: {file_path.name}")
                try:
                    result = self.transcribe(str(file_path))
                    result["file"] = file_path.name
                    results.append(result)
                except Exception as e:
                    print(f"失败 {file_path.name}: {e}")
                    
        # 汇总统计
        total_duration = sum(r.get("duration", 0) for r in results)
        total_chars = sum(r.get("char_count", 0) for r in results)
        
        summary = {
            "total_files": len(results),
            "total_duration_seconds": round(total_duration, 2),
            "total_chars": total_chars,
            "avg_chars_per_second": round(total_chars / total_duration, 2) if total_duration > 0 else 0,
            "results": results
        }
        
        # 写入输出
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"完成 {len(results)} 个文件 → {output_path}")
        return summary


def main():
    errors = check_dependencies()
    if errors:
        print(f"缺少依赖: {', '.join(errors)}")
        print("安装: pip install openai-whisper")
        return
        
    parser = argparse.ArgumentParser(description="语音消息解析器")
    parser.add_argument("--input", "-i", required=True, help="语音文件或目录")
    parser.add_argument("--output", "-o", required=True, help="输出JSON路径")
    parser.add_argument("--model", "-m", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper模型 (默认: base)")
    parser.add_argument("--language", "-l", default="zh", help="语言 (默认: zh)")
    parser.add_argument("--batch", "-b", action="store_true", help="批量处理目录")
    
    args = parser.parse_args()
    
    vp = VoiceParser(model_size=args.model)
    
    if args.batch:
        vp.process_batch(args.input, args.output)
    else:
        result = vp.transcribe(args.input, args.language)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"转录完成 → {args.output}")
        print(f"文本: {result['text'][:100]}...")


if __name__ == "__main__":
    main()
