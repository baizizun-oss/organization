# AudioProcessService.py
import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


class AudioProcessService():
    """
    封装基于 FunASR 的本地语音转文字服务。
    支持 m4a/mp3/wav/flac 等格式（依赖 ffmpeg）。
    假设 ASR 依赖（funasr, modelscope, pydub）已安装在当前 Python 环境中。
    """

    MODEL_ID = "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
    SUPPORTED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()
        self.python_exe = Path(sys.executable)  # 直接使用当前 Python
        self._initialized = False

    def _run_cmd(self, cmd, **kwargs):
        """安全运行命令，捕获异常"""
        try:
            return subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(map(str, cmd))}\nstderr: {e.stderr}")
            raise RuntimeError(f"Subprocess error: {e.stderr}") from e

    def _has_nvidia_gpu(self) -> bool:
        return shutil.which("nvidia-smi") is not None

    def _ensure_ffmpeg(self):
        if shutil.which("ffmpeg") is None:
            raise EnvironmentError(
                "FFmpeg 未安装。请先安装 ffmpeg：\n"
                "  Ubuntu/Debian: sudo apt install -y ffmpeg\n"
                "  macOS: brew install ffmpeg\n"
                "  Windows: https://www.gyan.dev/ffmpeg/builds/ 并加入 PATH"
            )
        logger.info("✅ ffmpeg 已检测到")

    def _ensure_deps(self):
        """确保当前环境中已安装必要的 ASR 依赖"""
        if self._initialized:
            return

        missing = []
        for pkg in ["funasr", "modelscope", "pydub"]:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)

        if missing:
            raise RuntimeError(
                f"缺少 ASR 依赖包: {', '.join(missing)}。\n"
                f"请在当前虚拟环境中运行:\n"
                f"  pip install {' '.join(missing)} -i https://pypi.tuna.tsinghua.edu.cn/simple"
            )

        logger.info("✅ ASR 依赖已就绪")
        self._initialized = True

    def transcribe(self, input_audio: str, output_txt: Optional[str] = None) -> str:
        """
        将音频文件转为文字。
        :param input_audio: 输入音频路径（支持 m4a/mp3/wav 等）
        :param output_txt: 可选，输出文本路径；若未提供，则返回文本内容
        :return: 转写后的文本
        """
        input_path = Path(input_audio).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"输入音频不存在: {input_path}")

        _, ext = os.path.splitext(input_path.name.lower())
        if ext not in self.SUPPORTED_EXTENSIONS:
            logger.warning(f"⚠️ 非标准扩展名 {ext}，但若 ffmpeg 支持仍可尝试")

        self._ensure_ffmpeg()
        self._ensure_deps()

        # 启动子进程调用独立脚本（避免主进程加载 torch）
        script_content = self._get_transcribe_script()
        script_path = self.base_dir / "asr_worker.py"
        script_path.write_text(script_content, encoding="utf-8")

        temp_wav = input_path.with_suffix(".temp.wav")
        cmd = [
            str(self.python_exe),
            str(script_path),
            "--model_id", self.MODEL_ID,
            "--input", str(input_path),
            "--temp_wav", str(temp_wav)
        ]

        try:
            result = self._run_cmd(cmd)
            transcript = result.stdout.strip()
        finally:
            # 清理临时文件
            if temp_wav.exists():
                temp_wav.unlink()
            if script_path.exists():
                script_path.unlink()

        if output_txt:
            Path(output_txt).write_text(transcript, encoding="utf-8")
            logger.info(f"📄 转写结果已保存至: {output_txt}")

        return transcript

    def _get_transcribe_script(self) -> str:
        """返回一个独立的 ASR 执行脚本内容（避免主进程加载 torch）"""
        return f'''
import sys
import os
from pydub import AudioSegment
from funasr import AutoModel
import torch

input_path = sys.argv[sys.argv.index("--input") + 1]
temp_wav = sys.argv[sys.argv.index("--temp_wav") + 1]
model_id = sys.argv[sys.argv.index("--model_id") + 1]

# 预处理音频
audio = AudioSegment.from_file(input_path)
if audio.channels > 1:
    audio = audio.set_channels(1)
audio = audio.set_frame_rate(16000)
audio.export(temp_wav, format="wav")

# 加载模型并转写
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = AutoModel(
    model=model_id,
    trust_remote_code=True,
    vad_model="fsmn-vad",
    punc_model="ct-punc",
    device=device
)
result = model.generate(input=str(temp_wav))
text = result[0]["text"] if isinstance(result, list) else str(result)
print(text)
'''    