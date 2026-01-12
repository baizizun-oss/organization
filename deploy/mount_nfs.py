#!/usr/bin/env python3
# mount_nfs.py
"""
挂载NFS目录的脚本
将远程服务器上的NFS目录挂载到本地的指定位置
"""

import os
import subprocess
from pathlib import Path


def run_cmd(cmd, desc=""):
    """执行系统命令"""
    if desc:
        print(f"▶️ {desc}")
    else:
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print(f"▶️ 执行: {cmd_str}")
    
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(f"✅ {result.stdout.strip() if result.stdout.strip() else '命令执行成功'}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        raise


def check_nfs_utils():
    """检查NFS客户端工具是否已安装"""
    try:
        # 检查nfs-common包是否已安装
        result = subprocess.run(['dpkg', '-l', 'nfs-common'], 
                               capture_output=True, text=True, check=True)
        return 'nfs-common' in result.stdout
    except subprocess.CalledProcessError:
        return False


def install_nfs_utils():
    """安装NFS客户端工具"""
    print("📦 正在安装NFS客户端工具...")
    try:
        run_cmd(["sudo", "apt", "update"])
        run_cmd(["sudo", "apt", "install", "-y", "nfs-common"])
        print("✅ NFS客户端工具安装完成")
    except Exception as e:
        print(f"❌ NFS客户端工具安装失败: {e}")
        raise


def check_nfs_mount(mount_point):
    """检查NFS是否已经挂载"""
    try:
        with open("/proc/mounts", "r") as f:
            mounts = f.read()
            return mount_point in mounts
    except Exception:
        return False


def check_directory_exists(path):
    """检查目录是否存在"""
    return os.path.exists(path)


def create_directory_if_not_exists(path):
    """创建目录（如果不存在）"""
    if not check_directory_exists(path):
        print(f"📁 创建目录: {path}")
        os.makedirs(path, exist_ok=True)
        return True
    else:
        print(f"✅ 目录已存在: {path}")
        return False


def mount_nfs_directory(nfs_server_path, local_mount_point):
    """挂载NFS目录"""
    NFS_SERVER_IP = "192.168.100.241"

    print(f"🔧 开始配置NFS挂载: {NFS_SERVER_IP}:{nfs_server_path} -> {local_mount_point}")
    
    # 检查并安装NFS客户端工具
    if not check_nfs_utils():
        install_nfs_utils()
    else:
        print("✅ NFS客户端工具已安装")
    
    # 创建本地挂载点
    create_directory_if_not_exists(local_mount_point)
    
    # 检查是否已经挂载
    if check_nfs_mount(local_mount_point):
        print(f"✅ {local_mount_point} 已经挂载，无需重复挂载")
        return True
    
    # 检查与NFS服务器的连通性
    print(f"🔍 检查与NFS服务器 {NFS_SERVER_IP} 的连通性...")
    ping_result = subprocess.run(['ping', '-c', '1', NFS_SERVER_IP], capture_output=True)
    if ping_result.returncode != 0:
        print(f"⚠️ 无法连接到NFS服务器 {NFS_SERVER_IP}")
        print("请确保网络连通性和NFS服务器正常运行")
        return False
    
    # 执行挂载
    try:
        print(f" mounting {NFS_SERVER_IP}:{nfs_server_path} 到 {local_mount_point}")
        cmd = ["sudo", "mount", "-t", "nfs", f"{NFS_SERVER_IP}:{nfs_server_path}", local_mount_point]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ NFS挂载成功: {NFS_SERVER_IP}:{nfs_server_path} -> {local_mount_point}")
        
        # 验证挂载
        if check_nfs_mount(local_mount_point):
            print("✅ 挂载验证成功")
            
            # 设置适当的权限
            run_cmd(["sudo", "chmod", "777", local_mount_point], f"设置挂载目录权限: {local_mount_point}")
            
            return True
        else:
            print("❌ 挂载验证失败")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ NFS挂载失败: {e}")
        print(f"错误详情: {e.stderr}")
        return False


def unmount_nfs_directory(local_mount_point):
    """卸载NFS目录"""
    if not check_nfs_mount(local_mount_point):
        print(f"⚠️ {local_mount_point} 当前未挂载")
        return True
    
    try:
        print(f"📤 正在卸载 {local_mount_point}")
        result = subprocess.run(["sudo", "umount", local_mount_point], 
                               capture_output=True, text=True, check=True)
        print(f"✅ NFS卸载成功: {local_mount_point}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ NFS卸载失败: {e}")
        print(f"错误详情: {e.stderr}")
        return False


def mount_all_nfs_directories():
    """挂载所有NFS目录"""
    # 定义需要挂载的NFS目录映射
    nfs_mounts = [
        {
            "nfs_path": "/home/bgp1984/projects/server_241/projects/organization_nfs_server/data/Works",
            "local_path": os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "organization", "templates", "Works", "upload"
            ),
            "description": "Works上传目录"
        },
        {
            "nfs_path": "/home/bgp1984/projects/server_241/projects/organization_nfs_server/data/Files",
            "local_path": os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "organization", "templates", "Files", "upload"
            ),
            "description": "Files上传目录"
        },
        {
            "nfs_path": "/home/bgp1984/projects/server_241/projects/organization_nfs_server/data/DB",
            "local_path": os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "db"
            ),
            "description": "数据库目录"
        }
    ]
    
    success_count = 0
    total_count = len(nfs_mounts)
    
    for mount_info in nfs_mounts:
        print(f"\n📁 正在挂载{mount_info['description']}...")
        if mount_nfs_directory(mount_info["nfs_path"], mount_info["local_path"]):
            success_count += 1
        else:
            print(f"⚠️ 挂载{mount_info['description']}失败")
    
    print(f"\n✅ 总共挂载了 {success_count}/{total_count} 个NFS目录")
    return success_count == total_count


def unmount_all_nfs_directories():
    """卸载所有NFS目录"""
    # 获取所有挂载点
    nfs_mounts = [
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "organization", "templates", "Works", "upload"
        ),
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "organization", "templates", "Files", "upload"
        ),
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "db"
        )
    ]
    
    success_count = 0
    total_count = len(nfs_mounts)
    
    for mount_point in nfs_mounts:
        if unmount_nfs_directory(mount_point):
            success_count += 1
        else:
            print(f"⚠️ 卸载 {mount_point} 失败")
    
    print(f"\n✅ 总共卸载了 {success_count}/{total_count} 个NFS目录")
    return success_count == total_count


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "unmount":
        success = unmount_all_nfs_directories()
    else:
        success = mount_all_nfs_directories()
    
    if not success:
        sys.exit(1)