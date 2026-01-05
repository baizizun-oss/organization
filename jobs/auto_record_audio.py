# jobs/auto_record_audio.py

import logging
import time
import myportal.common as common
from jobs.recorder import record_audio, save_audio
from .asr_client import transcribe_audio_file_async
from .llm_client import polish_transcript_async

logger = logging.getLogger(__name__)

# 👇 改为 async def
async def auto_record_and_transcribe():
    """
    定时任务：录音 → 保存 → 转写（调用远程 AI Server）→ 入库
    """
    logger.info("🔄 开始自动录音任务...")

    transcript = ""
    audio_path_str = ""
    status = "failed"
    processed_content = ""  # 👈 新增

    recording = record_audio(duration=90*60)
    
    if recording is not None:
        audio_path_str = save_audio(recording)
        if audio_path_str:
            try:
                transcript = await transcribe_audio_file_async(audio_path_str)  # ✅ await 异步调用
                status = "success"
            except Exception as e:
                transcript = f"[转写失败] {str(e)}"
                logger.exception("ASR 远程调用异常")

    if transcript is not None:

        try:
            processed_content = await polish_transcript_async(transcript)  # ✅ await 异步调用
            status = "success"
        except Exception as e:
            processed_content = f"[llm整理失败] {str(e)}"
            logger.exception("ASR 远程调用异常")


    # 写入数据库
    ctime = int(time.time())
    sql = """
        INSERT INTO record (raw_content,processed_content, audio, ctime)
        VALUES (?, ?, ?,?)
    """
    try:
        common.execute("organization", sql, (transcript,processed_content, audio_path_str, ctime))
        logger.info(f"✅ 自动录音任务完成 | 状态: {status}")
    except Exception as e:
        logger.error("❌ 数据库写入失败: %s", e)


