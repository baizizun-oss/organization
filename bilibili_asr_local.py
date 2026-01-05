#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

# --- 引入你的 ASR 客户端 ---
# 假设这个脚本和 jobs/asr_client.py 在同一目录，或已加入 PYTHONPATH
try:
    from jobs.asr_client import transcribe_audio_file_sync as transcribe_audio
except ImportError:
    # 如果不在 jobs/ 目录下，临时添加路径（可选）
    sys.path.append(str(Path(__file__).parent))
    from jobs.asr_client import transcribe_audio_file_sync as transcribe_audio

def convert_to_wav(input_path: str, output_path: str):
    """使用 ffmpeg 将任意音频转为 16k WAV（兼容大多数 ASR）"""
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-ar", "16000",      # 采样率 16kHz
        "-ac", "1",          # 单声道
        "-f", "wav",
        "-y",                # 覆盖输出
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg 转换失败: {e}")

def download_audio(url, output_dir):
    """使用 you-get 下载 B站音频（默认 m4a）"""
    print(f"📥 正在下载音频: {url}")
    cmd = [
        "you-get",
        "--extractor=bilibili",
        "--output-dir", output_dir,
        "--output-filename", "audio",
        "--format", "m4a",
        url
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        # 查找实际文件（you-get 可能加后缀）
        for f in Path(output_dir).glob("audio*.m4a"):
            return str(f)
        raise FileNotFoundError("未找到下载的音频文件")
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败: {e.stderr.decode()}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="B站视频 → 音频 → 调用本地 ASR 服务转文字")
    parser.add_argument("url", help="B站视频链接")

    args = parser.parse_args()
    url = args.url

    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"📁 临时目录: {tmp_dir}")

        # 1. 下载原始音频（m4a）
        raw_audio = download_audio(url, tmp_dir)

        # 2. 转为 WAV（适配你的 ASR）
        wav_path = os.path.join(tmp_dir, "audio.wav")
        print("🔄 正在转换为 WAV 格式...")
        convert_to_wav(raw_audio, wav_path)

        # 3. 调用你的本地 ASR 服务
        print("📤 正在调用本地 ASR 服务 (192.168.100.196:8081)...")
        text = transcribe_audio(raw_audio)

        # 4. 输出结果
        print("\n✅ 识别结果:\n")
        print(text)

        # 5. 保存到当前目录
        output_file = "bilibili_transcript.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n📄 已保存到: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()