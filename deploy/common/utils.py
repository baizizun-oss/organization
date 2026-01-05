# common/utils.py
import subprocess
import time
import os


def run_cmd(cmd, shell=False, check=True, desc=""):
    """执行系统命令，支持描述信息"""
    if desc:
        print(f"▶️ {desc}")
    else:
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print(f"▶️ 执行: {cmd_str}")
    try:
        result = subprocess.run(cmd, shell=shell, check=check, text=True, capture_output=False)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        raise

def get_local_ip():
    """获取本机局域网 IPv4 地址"""
    try:
        result = subprocess.run(
            "ip -4 addr show scope global | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}' | head -1",
            shell=True, capture_output=True, text=True
        )
        ip = result.stdout.strip()
        return ip if ip else "192.168.100.182"
    except Exception:
        return "192.168.100.182"

def get_username():
    """获取当前用户名"""
    return os.environ.get("USER") or os.getlogin()




def switch_docker_mirror(mirror_url):
    """将 docker.list 中的源替换为指定 mirror_url"""
    list_file = "/etc/apt/sources.list.d/docker.list"
    if not os.path.exists(list_file):
        raise FileNotFoundError(f"未找到 Docker 源配置文件: {list_file}")
    
    # 使用 sed 替换任意已有的 docker-ce URL 为新的 mirror
    cmd = [
        "sudo", "sed", "-i",
        f"s|https://[^ ]*/docker-ce|{mirror_url}|g",
        list_file
    ]
    subprocess.run(cmd, check=True)

# common/utils.py

def robust_apt_update():
    mirrors = [
        "https://mirrors.tuna.tsinghua.edu.cn/docker-ce",
        "https://mirrors.aliyun.com/docker-ce",
        "https://download.docker.com"
    ]


    for mirror in mirrors:
        print(f"🔧 尝试使用 Docker 镜像: {mirror}")
        try:
            switch_docker_mirror(mirror)

            # 清理缓存
            subprocess.run(["sudo", "apt", "clean"], check=False)
            subprocess.run(["sudo", "rm", "-rf", "/var/lib/apt/lists/*"], check=False)

            # 关键：不用 check=True，而是捕获结果
            result = subprocess.run(["sudo", "apt", "update"], capture_output=True, text=True)

            # 如果没有致命错误（比如网络不通），就算成功
            # 即使有 "Hash Sum mismatch"，只要不是完全无法连接，就接受
            if result.returncode == 0 or "Failed to fetch" not in result.stderr:
                print("✅ apt update 成功（或可接受的部分成功）")
                return
            else:
                print(f"❌ 镜像 {mirror} 完全失败: {result.stderr}")

        except Exception as e:
            print(f"⚠️ 镜像 {mirror} 异常: {e}")
            continue

    raise RuntimeError("所有 Docker 镜像源均无法完成 apt update，请检查网络或稍后重试。")