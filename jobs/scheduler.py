# jobs/scheduler.py

import logging
from datetime import datetime
from apscheduler.schedulers.tornado import TornadoScheduler

import jobs.auto_record_audio as auto_record_audio


logger = logging.getLogger(__name__)


async def audio_task():
    """定时执行录音+转写+入库"""
    logger.info(f"🎙️ 定时录音任务开始: {datetime.now()}")
    try:
        auto_record_audio.auto_record_and_transcribe()
        logger.info("✅ 定时录音任务成功完成")
    except Exception as e:
        logger.error(f"❌ 定时录音任务失败: {e}", exc_info=True)



scheduler = TornadoScheduler()

def init_scheduler():
    # 添加异步任务
    scheduler.add_job(
        auto_record_audio.auto_record_and_transcribe,
        'cron',
        day_of_week='thu',
        hour=12,
        minute=30,
        id='club_rec_thu_1230',
        replace_existing=True
    )
    # scheduler.add_job(
    #     auto_record_audio.auto_record_and_transcribe,
    #     'cron',
    #     day_of_week='fri',
    #     hour=22,
    #     minute=10,
    #     id='club_rec_fri_1230',
    #     replace_existing=True
    # )    
    scheduler.start()
    logger.info("✅ APScheduler (Tornado) 已启动")    