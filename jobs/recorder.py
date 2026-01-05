# jobs/recorder.py

import subprocess
import os
import logging
from datetime import datetime
import numpy as np
from scipy.io.wavfile import read, write
import myportal.common as common

RECORD_DIR = os.path.join(common.BASE_DIR, "jobs", "recordings")
os.makedirs(RECORD_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

def record_audio(duration=5):
    """
    使用 parecord + timeout 录音，返回 numpy 数组（int16, 单声道）或 None
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_wav = os.path.join(RECORD_DIR, f"temp_{timestamp}.wav")

    try:
        logger.info(f"🎙️ 开始录音 {duration} 秒（使用 parecord）...")
        
        # 使用 timeout 强制结束录音
        cmd = [
            'timeout', str(duration + 2),  # 多给 2 秒缓冲
            'parecord',
            '--rate', '16000',
            '--channels', '1',
            '--format', 's16le',
            temp_wav
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # timeout 正常终止返回码为 124，parecord 成功为 0
        if result.returncode not in (0, 124):
            logger.error(f"parecord 失败 (ret={result.returncode}): {result.stderr}")
            return None
        
        if not os.path.exists(temp_wav) or os.path.getsize(temp_wav) == 0:
            logger.warning("录音文件为空")
            return None

        # 读取音频数据
        sample_rate, audio_data = read(temp_wav)
        logger.info(f"✅ 录音成功: {len(audio_data)} samples (~{len(audio_data)/16000:.1f}s)")

        # 删除临时文件（save_audio 会另存）
        os.remove(temp_wav)

        return audio_data

    except Exception as e:
        logger.exception("录音异常: %s", e)
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        return None


def save_audio(recording, output_dir=RECORD_DIR):
    """
    保存录音为 WAV 文件（16kHz），返回文件路径
    """
    if recording is None or len(recording) == 0:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{timestamp}.wav"
    filepath = os.path.join(output_dir, filename)

    try:
        # ⚠️ 注意：必须用 16000 Hz（与录音一致），不要写 48000！
        write(filepath, 16000, recording)
        logger.info(f"💾 音频已保存: {filepath}")
        return filepath
    except Exception as e:
        logger.error("❌ 保存音频失败: %s", e)
        return None