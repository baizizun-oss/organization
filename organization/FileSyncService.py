import os
import logging
import sqlite3
import paramiko
from scp import SCPClient

class FileSyncService:
    def __init__(self):
        """初始化文件同步服务"""
        self.logger = logging.getLogger("FileSyncService")
        # 备份服务器配置
        self.backup_server = "192.168.100.184"  # 备份服务器IP地址
        self.backup_user = "bgp1984"            # 备份服务器用户名
        self.backup_password = "021415"  # 备份服务器密码（实际使用时替换）
        self.backup_path = "/home/bgp1984/projects/organization/organization/templates/File/upload/"  # 备份目录
        
    def sync_file(self, local_file_path, file_id):
        """
        主同步方法
        1. 更新数据库状态为"syncing"
        2. 传输文件到备份服务器
        3. 验证传输结果并更新状态
        """


        # 备份服务器配置
        self.backup_server = "192.168.100.184"  # 备份服务器IP地址
        self.backup_user = "bgp1984"            # 备份服务器用户名
        self.backup_password = "021415"  # 备份服务器密码（实际使用时替换）
        self.backup_path = "/home/bgp1984/projects/organization/organization/templates/File/upload/"  # 备份目录        
        try:
            # 更新数据库状态为"正在同步"
            self._update_sync_status(file_id, "syncing")
            
            # 传输文件到备份服务器
            self._scp_transfer(local_file_path)
            
            # 验证文件是否成功传输
            if self._verify_transfer(local_file_path):
                # 同步成功，更新状态
                self._update_sync_status(file_id, "success")
                self.logger.info(f"文件同步成功: {local_file_path}")
                return True
            else:
                # 同步失败，更新状态
                self._update_sync_status(file_id, "failed")
                self.logger.error(f"文件同步验证失败: {local_file_path}")
                return False
                
        except Exception as e:
            # 捕获异常并更新状态
            self._update_sync_status(file_id, "failed")
            self.logger.exception(f"文件同步失败: {str(e)}")
            return False
    
    def _scp_transfer(self, local_file_path):
        """
        使用SCP协议传输文件
        使用密码认证而非密钥
        """
        ssh = paramiko.SSHClient()
        # 自动添加主机密钥（生产环境应考虑安全性）
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # 使用密码连接服务器
            ssh.connect(
                self.backup_server,
                username=self.backup_user,
                password=self.backup_password
            )
            
            # 创建SCP客户端并传输文件
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(local_file_path, self.backup_path)
        finally:
            # 确保关闭连接
            ssh.close()
    
    def _verify_transfer(self, local_file_path):
        """
        验证文件是否成功传输
        通过比较本地和远程文件大小进行验证
        """
        # 获取本地文件大小
        local_size = os.path.getsize(local_file_path)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # 使用密码连接服务器
            ssh.connect(
                self.backup_server,
                username=self.backup_user,
                password=self.backup_password
            )
            
            # 获取远程文件大小
            filename = os.path.basename(local_file_path)
            remote_path = os.path.join(self.backup_path, filename)
            # 执行命令获取文件大小
            stdin, stdout, stderr = ssh.exec_command(f"stat -c %s {remote_path}")
            remote_size = int(stdout.read().strip())
            
            # 比较本地和远程文件大小
            return local_size == remote_size
        finally:
            # 确保关闭连接
            ssh.close()
    
    def _update_sync_status(self, file_id, status):
        """
        更新数据库中的同步状态
        """
        try:
            # 连接数据库
            conn = sqlite3.connect(os.path.join("db", "organization.db"))
            cursor = conn.cursor()
            # 更新文件同步状态
            cursor.execute(
                "UPDATE file SET sync_status = ? WHERE id = ?",
                (status, file_id)
            )
            conn.commit()
        except Exception as e:
            # 记录更新失败错误
            self.logger.error(f"更新同步状态失败: {str(e)}")
        finally:
            # 确保关闭数据库连接
            if conn:
                conn.close()
