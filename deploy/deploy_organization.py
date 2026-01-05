# projects/deploy_organization.py

import os
import shutil
import subprocess
import pwd
from pathlib import Path
from common.utils import run_cmd, get_username


def deploy_organization():
    print("\n🚀 部署 organization 原生服务（非 Docker，监听 9000）...")

    USERNAME = get_username()
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    ORG_PROJECT_DIR = os.path.join(SCRIPT_DIR, "..","..","organization")
    AUDIO_PROCESS_SERVICE_PATH = os.path.join(ORG_PROJECT_DIR, "organization_admin", "AudioProcessService.py")

    VENV_DIR = os.path.join(ORG_PROJECT_DIR, "venv")
    PYTHON_SCRIPT = os.path.join(ORG_PROJECT_DIR, "app.py")
    FILE_UPLOAD_DIR = os.path.join(ORG_PROJECT_DIR, "organization/templates/File/upload")
    WORKS_UPLOAD_DIR = os.path.join(ORG_PROJECT_DIR, "organization/templates/Works/upload")

    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted_host = "pypi.tuna.tsinghua.edu.cn"

    # ✅ 第一步：确保项目目录存在
    if not os.path.exists(ORG_PROJECT_DIR):
        raise FileNotFoundError(f"项目目录不存在: {ORG_PROJECT_DIR}")

    # ✅ 第二步：安装系统依赖
    print("📦 安装系统依赖...")
    run_cmd(["sudo", "apt-get", "update"])
    run_cmd(["sudo", "apt-get", "install", "-y",
             "python3-venv", "portaudio19-dev", "redis-server", "ffmpeg"])

    # ✅ 第三步：启动 redis
    run_cmd(["sudo", "systemctl", "enable", "--now", "redis-server"])

    # ✅ 第四步：创建或修复虚拟环境
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
    if not os.path.exists(VENV_PYTHON):
        print("⚠️  虚拟环境缺失或损坏，正在重建...")
        if os.path.exists(VENV_DIR):
            shutil.rmtree(VENV_DIR)
        print("✅ 创建新的虚拟环境...")
        run_cmd(["python3", "-m", "venv", VENV_DIR])
    else:
        print("✅ 虚拟环境已存在且有效")

    pip_bin = os.path.join(VENV_DIR, "bin", "pip")
    python_bin = VENV_PYTHON

    # ✅ 第五步：升级 pip 并清理缓存
    print("⏫ 升级 pip 到最新版本...")
    run_cmd([pip_bin, "install", "--upgrade", "pip",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "cache", "purge"])

    # ✅ 第六步：确保上传目录存在
    for local_dir in [FILE_UPLOAD_DIR, WORKS_UPLOAD_DIR]:
        os.makedirs(local_dir, exist_ok=True)
        run_cmd(["chown", f"{USERNAME}:{USERNAME}", local_dir])

    # ✅ 第七步：安装 Python 依赖（含 ASR 所需）
    print("📥 安装 Python 依赖...")
    
    # 安装 faster-whisper 相关（保留原有逻辑）
    run_cmd([pip_bin, "install", "tokenizers==0.19.1",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "faster-whisper", "--no-deps",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "ctranslate2", "huggingface-hub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 👇 新增：安装 FunASR 所需依赖（用于 AudioProcessService）
    print("📦 安装 FunASR 语音识别依赖...")
    run_cmd([pip_bin, "install", "funasr", "modelscope", "pydub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 其他通用 Python 包
    PYTHON_PACKAGES = [
        "tornado", "requests", "opencv-python", "apscheduler",
        "redis", "sounddevice", "scipy", "SpeechRecognition",
        "paramiko", "scp","aiohttp"
    ]
    for pkg in PYTHON_PACKAGES:
        run_cmd([pip_bin, "install", pkg,
                 "-i", index_url, "--trusted-host", trusted_host])


    # ✅ 第十步：释放端口并启动服务
    print("⚠️  释放 9000 端口（如果被占用）...")
    subprocess.run("fuser -k 9000/tcp || true", shell=True)

    log_file = os.path.join(ORG_PROJECT_DIR, "logs", "organization.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 启动环境变量（用于 app.py 和子进程）
    env = os.environ.copy()

    env["LANG"] = "zh_CN.UTF-8"
    env["LC_ALL"] = "zh_CN.UTF-8"

    cmd = [python_bin, PYTHON_SCRIPT]
    print(f"✅ 启动 organization 服务（监听 9000，日志: {log_file}）...")
    with open(log_file, "a") as log:
        subprocess.Popen(cmd, cwd=ORG_PROJECT_DIR, stdout=log, stderr=log, env=env)

    print("✅ organization 原生服务已启动（后台运行）")


if __name__ == "__main__":
    deploy_organization()