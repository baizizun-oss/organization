# projects/organization/deploy/services/install_python_deps.py

import os
from common.utils import run_cmd, get_username


def upgrade_pip(venv_dir):
    """升级pip到最新版本并清理缓存"""
    pip_bin = os.path.join(venv_dir, "bin", "pip")
    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted_host = "pypi.tuna.tsinghua.edu.cn"
    
    print("⏫ 升级 pip 到最新版本...")
    run_cmd([pip_bin, "install", "--upgrade", "pip",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "cache", "purge"])


def create_upload_directories(org_project_dir):
    """创建上传目录"""
    USERNAME = get_username()
    FILE_UPLOAD_DIR = os.path.join(org_project_dir, "organization/templates/File/upload")
    WORKS_UPLOAD_DIR = os.path.join(org_project_dir, "organization/templates/Works/upload")
    
    for local_dir in [FILE_UPLOAD_DIR, WORKS_UPLOAD_DIR]:
        os.makedirs(local_dir, exist_ok=True)
        run_cmd(["chown", f"{USERNAME}:{USERNAME}", local_dir])


def install_python_dependencies(venv_dir):
    """安装Python依赖包"""
    pip_bin = os.path.join(venv_dir, "bin", "pip")
    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted_host = "pypi.tuna.tsinghua.edu.cn"
    
    # 安装 faster-whisper 相关
    print("📥 安装 faster-whisper 相关依赖...")
    run_cmd([pip_bin, "install", "tokenizers==0.19.1",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "faster-whisper", "--no-deps",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "ctranslate2", "huggingface-hub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 安装 FunASR 所需依赖（用于 AudioProcessService）
    print("📦 安装 FunASR 语音识别依赖...")
    run_cmd([pip_bin, "install", "funasr", "modelscope", "pydub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 其他通用 Python 包
    PYTHON_PACKAGES = [
        "tornado", "requests", "opencv-python", "apscheduler",
        "redis", "sounddevice", "scipy", "SpeechRecognition",
        "paramiko", "scp", "aiohttp"
    ]
    
    print("📥 安装其他 Python 依赖...")
    for pkg in PYTHON_PACKAGES:
        run_cmd([pip_bin, "install", pkg,
                 "-i", index_url, "--trusted-host", trusted_host])