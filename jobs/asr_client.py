# jobs/asr_client.py
import logging
import asyncio
import aiohttp
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

ASR_API_URL = "http://192.168.100.196:8081/asr"  # 统一配置


async def transcribe_audio_file_async(audio_path: str) -> str:
    """
    异步调用远程 ASR（用于 jobs/ 定时任务）
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    try:
        async with aiohttp.ClientSession() as session:
            with open(audio_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('audio', f, filename=audio_path.name, content_type='audio/wav')
                logger.info(f"📤 [Async] 调用 ASR 服务: {ASR_API_URL}")
                async with session.post(ASR_API_URL, data=data, timeout=60) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("text", "").strip()
                    else:
                        error_text = await resp.text()
                        raise RuntimeError(f"ASR API 错误 [{resp.status}]: {error_text}")
    except Exception as e:
        logger.exception("ASR 异步调用失败")
        raise


def transcribe_audio_file_sync(audio_path: str) -> str:
    """
    同步调用远程 ASR（用于 Tornado Web handler）
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    try:
        with open(audio_path, 'rb') as f:
            files = {'audio': (audio_path.name, f, 'audio/wav')}
            logger.info(f"📤 [Sync] 调用 ASR 服务: {ASR_API_URL}")
            resp = requests.post(ASR_API_URL, files=files, timeout=60)
            if resp.status_code == 200:
                result = resp.json()
                return result.get("text", "").strip()
            else:
                raise RuntimeError(f"ASR API 错误 [{resp.status_code}]: {resp.text}")
    except Exception as e:
        logger.exception("ASR 同步调用失败")
        raise