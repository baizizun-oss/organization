import tornado.ioloop
import tornado.web
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.redis import RedisJobStore  # 可选，用于任务持久化
from datetime import datetime
import sounddevice as sd  # 用于录音
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr  # 用于语音识别
import os
import logging
import myportal.common as common
import subprocess
import asyncio


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化全局调度器变量
scheduler = None

# 录音参数
FS = 44100  # 采样率
SECONDS = 60  # 录音时长：1800秒（30分钟），根据社团活动时长调整
FILENAME_PREFIX = "club_meeting"

# 在文件顶部添加一个常量定义保存目录
AUDIO_SAVE_DIR = os.path.join(common.BASE_DIR,"record_mic")

# 确保目录存在
if not os.path.exists(AUDIO_SAVE_DIR):
    os.makedirs(AUDIO_SAVE_DIR)




# 修改 speech_to_text 函数中的文件保存部分
def speech_to_text(filename):
    """将录音文件转换为文字"""
    if not filename or not os.path.exists(filename):
        logging.error("音频文件不存在，无法进行识别")
        return
    
    logging.info("开始语音识别...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='zh-CN')  # 使用Google识别引擎，中文
            logging.info(f"识别结果: {text}")
            # 这里可以将识别结果保存到文件或数据库
            text_filename = f"{filename}.txt"
            with open(text_filename, "w", encoding='utf-8') as f:
                f.write(text)
            return text
    except sr.UnknownValueError:
        logging.error("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        logging.error(f"语音识别过程中出现错误: {e}")


async def audio_task():
    logger.info(f"音频任务在 {datetime.now()} 被触发")
    
    venv_python_path = "/home/bgp1984/env/organization/bin/python3"
    script_path = "/home/bgp1984/projects/organization/recorder.py"
    
    command = ["sudo",venv_python_path, script_path]  # 去掉 sudo

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    # ✅ 打印输出，方便调试
    if stdout:
        logger.info(f"录音脚本 stdout: {stdout.decode()}")
    if stderr:
        logger.error(f"录音脚本 stderr: {stderr.decode()}")
    
    if process.returncode == 0:
        logger.info("录音任务成功完成")
    else:
        logger.error(f"录音任务失败，返回码: {process.returncode}")

def init_scheduler():
    """初始化调度器"""
    global scheduler
    # 配置作业存储（这里使用内存存储，也可配置Redis持久化）
    jobstores = {
        'default': RedisJobStore(
            jobs_key='tornado_jobs', 
            run_times_key='tornado_runtimes',
            host='localhost',  # Redis服务器地址
            port=6379         # Redis端口
        )
    }
    
    scheduler = TornadoScheduler(
        jobstores=jobstores, 
        timezone='Asia/Shanghai'  # 设置时区
    )
    
    # 添加定时录音任务：每周四12:30执行
    scheduler.add_job(
        audio_task, 
        'cron', 
        day_of_week='wed', 
        hour=18, 
        minute=45,
        id='weekly_club_recording',
        replace_existing=True  # 如果任务已存在则替换
    )
    scheduler.add_job(
        audio_task, 
        'cron', 
        day_of_week='thu', 
        hour=11, 
        minute=19,
        id='weekly_club_recording',
        replace_existing=True  # 如果任务已存在则替换
    )    
    scheduler.add_job(
        audio_task, 
        'cron', 
        day_of_week='sun', 
        hour=14, 
        minute=59,
        id='weekly_club_recording',
        replace_existing=True  # 如果任务已存在则替换
    )        
    scheduler.start()
    logging.info("定时任务调度器已启动...")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Club Activity Recording Service is Running!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])



# if __name__ == "__main__":
#     # 初始化调度器
#     init_scheduler()
    
#     # 创建并启动Tornado应用
#     app = make_app()
#     app.listen(8888)
#     logging.info("Tornado服务启动在 8888 端口...")
    
#     # 启动IOLoop
#     tornado.ioloop.IOLoop.current().start()