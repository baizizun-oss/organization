# RemoveMemberService.py
import sqlite3
from datetime import datetime
import os
import myportal.common as common

class RemoveMemberService:
    
    @staticmethod
    def get_should_remove_members():
        """
        识别连续三次未签到的成员
        返回: list of tuple, 格式为 (user_id, user_name)
        """
        to_remove = []

        # 获取所有活跃用户
        active_users = common.select("organization", "SELECT id, name FROM user WHERE status != '已被除名'")
        
        for user in active_users:
            user_id = user["id"]
            user_name = user["name"]
            
            # 获取统计缺勤的开始时间
            check_start_time = RemoveMemberService._get_check_start_time(user_id)
            
            # 获取签到记录
            signin_records = RemoveMemberService._get_signin_records(user_id, check_start_time)
            
            # 检查连续缺勤
            if RemoveMemberService._check_consecutive_absence(signin_records):
                to_remove.append((user_id, user_name))
                
        return to_remove

    @staticmethod
    def _get_check_start_time(user_id):
        """
        获取用户的统计起始时间：
        - 如果有恢复历史，从最近一次正常的时间开始
        - 否则从最早记录开始（返回0）
        """
        sql = "SELECT ctime FROM user_status_history WHERE user_id = " + str(user_id) + " AND status = '正常' ORDER BY ctime DESC LIMIT 1"
        result = common.find("organization", sql)
        
        if result:
            return result["ctime"]
        else:
            # 如果没有除名历史，返回0表示从最早记录开始
            return 0

    @staticmethod
    def _get_signin_records(user_id, check_start_time):
        """
        获取用户从统计起始时间后的签到记录
        返回: list of (date, status)
        """
        # 获取观察期内的所有预期签到日期
        sql_dates = "SELECT expected_signin_time FROM signin_plan WHERE expected_signin_time >= " + str(check_start_time) + " ORDER BY expected_signin_time"
        expected_results = common.select("organization", sql_dates)
        
        # 获取用户的实际签到记录
        sql_signed = "SELECT DISTINCT strftime('%Y-%m-%d', click_time, 'unixepoch') as sign_date FROM click WHERE user_id = " + str(user_id) + " AND click_time >= " + str(check_start_time)
        signed_results = common.select("organization", sql_signed)
        
        # 将签到日期转换为集合以便快速查找
        signed_dates_set = set()
        for record in signed_results:
            signed_dates_set.add(record["sign_date"])
        
        # 构建签到状态记录
        records = []
        for date_record in expected_results:
            expected_timestamp = date_record["expected_signin_time"]
            expected_date = datetime.fromtimestamp(expected_timestamp).strftime('%Y-%m-%d')
            
            # 判断是否签到
            if expected_date in signed_dates_set:
                status = '已签到'
            else:
                status = '未签到'
                
            records.append((expected_date, status))
        
        return records

    @staticmethod
    def _check_consecutive_absence(records):
        """
        检查签到记录中是否有连续三次未签到
        返回: bool
        """
        consecutive_miss = 0
        
        for record in records:
            date = record[0]
            status = record[1]
            
            if status == '未签到':
                consecutive_miss = consecutive_miss + 1
                if consecutive_miss >= 3:
                    return True
            else:
                consecutive_miss = 0  # 重置连续未签到计数
        
        return False

    @staticmethod
    def remove_member(user_id):
        """
        将指定用户的状态更新为'已被除名'
        返回: bool, 表示操作是否成功
        """
        sql = "UPDATE user SET status = '已被除名' WHERE id = " + str(user_id)
        
        try:
            result = common.execute("organization", sql)
            if result:
                print("[RemoveMemberService] 用户 " + str(user_id) + " 除名成功")
                return True
            else:
                print("[RemoveMemberService] 用户 " + str(user_id) + " 除名失败")
                return False
        except Exception as e:
            print("[RemoveMemberService] 除名用户 " + str(user_id) + " 时出错: " + str(e))
            return False