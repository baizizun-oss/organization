# projects/organization/deploy/services/start_service.py

import os
import subprocess
from common.utils import run_cmd


def start_organization_service(org_project_dir, venv_dir, python_script):
    """启动organization服务"""
    # 释放端口并启动服务
    print("⚠️  释放 9000 端口（如果被占用）...")
    subprocess.run("fuser -k 9000/tcp || true", shell=True)

    # 创建日志目录
    log_file = os.path.join(org_project_dir, "logs", "organization.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 启动环境变量（用于 app.py 和子进程）
    env = os.environ.copy()
    env["LANG"] = "zh_CN.UTF-8"
    env["LC_ALL"] = "zh_CN.UTF-8"

    python_bin = os.path.join(venv_dir, "bin", "python")
    cmd = [python_bin, python_script]
    
    print(f"✅ 启动 organization 服务（监听 9000，日志: {log_file}）...")
    with open(log_file, "a") as log:
        subprocess.Popen(cmd, cwd=org_project_dir, stdout=log, stderr=log, env=env)

    print("✅ organization 原生服务已启动（后台运行）")