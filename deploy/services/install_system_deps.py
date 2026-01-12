# projects/organization/deploy/services/install_system_deps.py

import os
from common.utils import run_cmd


def install_system_dependencies():
    """安装系统依赖"""
    print("📦 安装系统依赖...")
    run_cmd(["sudo", "apt-get", "update"])
    run_cmd(["sudo", "apt-get", "install", "-y",
             "python3-venv", "portaudio19-dev", "redis-server", "ffmpeg"])


def start_redis_service():
    """启动redis服务"""
    print("🔄 启动 Redis 服务...")
    run_cmd(["sudo", "systemctl", "enable", "--now", "redis-server"])