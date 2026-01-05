# RecordController.py
import os
import time
from pathlib import Path
import tornado.web
import myportal.common as common
# from organization_admin.AudioProcessService import AudioProcessService
import logging
from jobs.asr_client import transcribe_audio_file_sync 
from jobs.llm_client import polish_transcript_sync

logger = logging.getLogger(__name__)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        records = common.select("organization", "SELECT * FROM record")
        self.render(
            os.path.join(common.BASE_DIR, "organization", "templates", "Record", "lists.html"),
            records=records
        )



