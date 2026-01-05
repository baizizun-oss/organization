# jobs/llm_client.py
import logging
import asyncio
import aiohttp
import requests

logger = logging.getLogger(__name__)

LLM_API_URL = "http://192.168.100.196:8082/polish"

async def polish_transcript_async(text: str) -> str:
    if not text or "[转写失败]" in text:
        return text
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(LLM_API_URL, json={"text": text}, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("polished", text)
                else:
                    logger.warning(f"LLM API 错误 [{resp.status}]: {await resp.text()}")
                    return text
    except Exception as e:
        logger.exception("LLM 异步调用失败")
        return text

def polish_transcript_sync(text: str) -> str:
    if not text or "[转写失败]" in text:
        return text
    try:
        resp = requests.post(LLM_API_URL, json={"text": text}, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("polished", text)
        else:
            logger.warning(f"LLM API 错误 [{resp.status_code}]: {resp.text}")
            return text
    except Exception as e:
        logger.exception("LLM 同步调用失败")
        return text