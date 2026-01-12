# deploy package initialization
# services package initialization
"""
服务启动模块
"""

import os
import subprocess
from common.utils import run_cmd


def start_organization_service(project_dir, venv_dir, python_script):
    """启动 organization 服务"""
    print("⚠️  释放 9000 端口（如果被占用）...")
    subprocess.run("fuser -k 9000/tcp || true", shell=True)

    log_file = os.path.join(project_dir, "logs", "organization.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 启动环境变量
    env = os.environ.copy()
    env["LANG"] = "zh_CN.UTF-8"
    env["LC_ALL"] = "zh_CN.UTF-8"

    python_bin = os.path.join(venv_dir, "bin", "python")
    cmd = [python_bin, python_script]
    
    print(f"✅ 启动 organization 服务（监听 9000，日志: {log_file}）...")
    with open(log_file, "a") as log:
        subprocess.Popen(cmd, cwd=project_dir, stdout=log, stderr=log, env=env)

    print("✅ organization 原生服务已启动（后台运行）")
"""
Python 依赖安装模块
"""

import os
from pathlib import Path
from common.utils import run_cmd, get_username


def upgrade_pip(venv_dir):
    """升级 pip"""
    print("⏫ 升级 pip 到最新版本...")
    pip_bin = os.path.join(venv_dir, "bin", "pip")
    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted_host = "pypi.tuna.tsinghua.edu.cn"
    
    run_cmd([pip_bin, "install", "--upgrade", "pip",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "cache", "purge"])


def create_upload_directories(project_dir):
    """创建上传目录"""
    print("✅ 第六步：确保上传目录存在")
    USERNAME = get_username()
    FILE_UPLOAD_DIR = os.path.join(project_dir, "organization/templates/File/upload")
    WORKS_UPLOAD_DIR = os.path.join(project_dir, "organization/templates/Works/upload")
    
    for local_dir in [FILE_UPLOAD_DIR, WORKS_UPLOAD_DIR]:
        os.makedirs(local_dir, exist_ok=True)
        run_cmd(["chown", f"{USERNAME}:{USERNAME}", local_dir])


def install_python_dependencies(venv_dir):
    """安装 Python 依赖"""
    print("📥 安装 Python 依赖...")
    pip_bin = os.path.join(venv_dir, "bin", "pip")
    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted_host = "pypi.tuna.tsinghua.edu.cn"

    # 安装 faster-whisper 相关
    run_cmd([pip_bin, "install", "tokenizers==0.19.1",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "faster-whisper", "--no-deps",
            "-i", index_url, "--trusted-host", trusted_host])
    run_cmd([pip_bin, "install", "ctranslate2", "huggingface-hub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 安装 FunASR 语音识别依赖
    print("📦 安装 FunASR 语音识别依赖...")
    run_cmd([pip_bin, "install", "funasr", "modelscope", "pydub",
            "-i", index_url, "--trusted-host", trusted_host])

    # 安装其他通用 Python 包
    PYTHON_PACKAGES = [
        "tornado", "requests", "opencv-python", "apscheduler",
        "redis", "sounddevice", "scipy", "SpeechRecognition",
        "paramiko", "scp", "aiohttp"
    ]
    for pkg in PYTHON_PACKAGES:
        run_cmd([pip_bin, "install", pkg,
                 "-i", index_url, "--trusted-host", trusted_host])
"""
虚拟环境管理模块
"""

import os
import shutil
from common.utils import run_cmd


def setup_virtual_environment(project_dir):
    """
    设置虚拟环境
    Returns:
        venv_dir: 虚拟环境路径
    """
    venv_dir = os.path.join(project_dir, "venv")
    venv_python = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_python):
        print("⚠️  虚拟环境缺失或损坏，正在重建...")
        if os.path.exists(venv_dir):
            shutil.rmtree(venv_dir)
        print("✅ 创建新的虚拟环境...")
        run_cmd(["python3", "-m", "venv", venv_dir])
    else:
        print("✅ 虚拟环境已存在且有效")
    
    return venv_dir
"""
系统依赖安装模块
"""

from common.utils import run_cmd


def install_system_dependencies():
    """安装系统依赖"""
    print("📦 安装系统依赖...")
    run_cmd(["sudo", "apt-get", "update"])
    run_cmd(["sudo", "apt-get", "install", "-y",
             "python3-venv", "portaudio19-dev", "redis-server", "ffmpeg"])


def start_redis_service():
    """启动 Redis 服务"""
    run_cmd(["sudo", "systemctl", "enable", "--now", "redis-server"])
# projects/organization/deploy/deploy_organization.py

import os
import subprocess
from common.utils import run_cmd, get_username

# 导入各个服务模块
from .services.install_system_deps import install_system_dependencies, start_redis_service
from .services.manage_venv import setup_virtual_environment
from .services.install_python_deps import upgrade_pip, create_upload_directories, install_python_dependencies
from .services.start_service import start_organization_service
from .mount_nfs import mount_all_nfs_directories


def deploy_organization():
    print("\n🚀 部署 organization 原生服务（非 Docker，监听 9000）...")

    USERNAME = get_username()
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"✅ 脚本目录: {SCRIPT_DIR}")
    ORG_PROJECT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "organization")
    print(f"✅ 项目目录: {ORG_PROJECT_DIR}")
    PYTHON_SCRIPT = os.path.join(ORG_PROJECT_DIR, "app.py")

    # 检查项目目录是否存在
    if not os.path.exists(ORG_PROJECT_DIR):
        raise FileNotFoundError(f"项目目录不存在: {ORG_PROJECT_DIR}")

    # 步骤1: 安装系统依赖
    install_system_dependencies()

    # 步骤2: 启动redis服务
    start_redis_service()

    # 步骤3: 设置虚拟环境
    venv_dir = setup_virtual_environment(ORG_PROJECT_DIR)

    # 步骤4: 升级pip
    upgrade_pip(venv_dir)

    # 步骤5: 创建上传目录
    create_upload_directories(ORG_PROJECT_DIR)

    # 步骤6: 挂载NFS目录（Works, Files, DB）
    print("\n📁 挂载NFS目录...")
    mount_all_nfs_directories()

    # 步骤7: 安装Python依赖
    install_python_dependencies(venv_dir)

    # 步骤8: 启动服务
    start_organization_service(ORG_PROJECT_DIR, venv_dir, PYTHON_SCRIPT)


if __name__ == "__main__":
    deploy_organization()