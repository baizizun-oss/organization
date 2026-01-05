# RecordController.py
import os
import time
from pathlib import Path
import tornado.web
import myportal.common as common
import logging
from jobs.asr_client import transcribe_audio_file_sync 
from jobs.llm_client import polish_transcript_sync
import config

logger = logging.getLogger(__name__)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        records = common.select("organization", "SELECT * FROM record")
        #处理音频文件路径
        for record in records:
            record["audio"] = filename = os.path.basename(record["audio"])


        self.render(
            os.path.join(common.BASE_DIR, "organization_admin", "templates", "Record", "lists.html"),
            records=records
        )


class addHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('<form method="post" enctype="multipart/form-data">'
        #            '<input type="file" name="audio" accept=".wav,.mp3,.m4a,.flac">'
        #            '<button type="submit">上传并转写</button>'
        #            '</form>')
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Record","add.html"))
        
    def post(self):
        transcript = "[转写失败：未知错误]"
        audio_path_str = ""
        status = "failed"
        processed_content = ""  # 👈 新增

        try:
            upload_file = self.request.files.get('audio')
            if not upload_file:
                self.set_status(400)
                self.write({"error": "缺少音频文件"})
                return

            file_info = upload_file[0]
            original_fname = file_info['filename']
            file_body = file_info['body']

            _, ext = os.path.splitext(original_fname.lower())
            if ext not in {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}:
                self.set_status(400)
                self.write({"error": f"不支持的音频格式: {ext}"})
                return

            timestamp = int(time.time())
            safe_name = f"rec_{timestamp}{ext}"
            recordings_dir = Path(common.BASE_DIR) / "recordings"
            recordings_dir.mkdir(exist_ok=True)
            save_path = recordings_dir / safe_name

            with open(save_path, 'wb') as f:
                f.write(file_body)

            # === 关键修改：调用远程 ASR（同步）===
            transcript = transcribe_audio_file_sync(str(save_path))
            processed_content= polish_transcript_sync(transcript)
            audio_path_str = str(save_path)
            status = "success"
            title = self.get_argument("title")

        except Exception as e:
            transcript = f"[转写或者整理失败] {str(e)}"
            logger.exception("上传转写或整理异常")

        finally:
            ctime = int(time.time())
            sql = "INSERT INTO record (raw_content,processed_content, audio, ctime,title) VALUES (?, ?, ?,?,?)"
            try:
                common.execute("organization", sql, (transcript,processed_content, audio_path_str, ctime,title))
            except Exception as e:
                logger.error("❌ 数据库写入失败: %s", e)

        if status == "success":
            self.write({
                "status": "success",
                "transcript": transcript,
                "file": audio_path_str
            })
        else:
            self.set_status(500)
            self.write({
                "status": "failed",
                "error": transcript
            })            



