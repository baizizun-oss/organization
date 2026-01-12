# projects/organization/deploy/services/manage_venv.py

import os
import shutil
from common.utils import run_cmd, get_username


def setup_virtual_environment(org_project_dir):
    """设置虚拟环境"""
    VENV_DIR = os.path.join(org_project_dir, "venv")
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
    
    # 检查虚拟环境是否存在且有效
    if not os.path.exists(VENV_PYTHON):
        print("⚠️  虚拟环境缺失或损坏，正在重建...")
        if os.path.exists(VENV_DIR):
            shutil.rmtree(VENV_DIR)
        print("✅ 创建新的虚拟环境...")
        run_cmd(["python3", "-m", "venv", VENV_DIR])
    else:
        print("✅ 虚拟环境已存在且有效")
        
    return VENV_DIR