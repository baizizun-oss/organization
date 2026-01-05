import sqlite3
import time
#import androidhelper
import os


    
BASE_DIR = os.path.join(os.path.dirname(__file__),"..")
#获取远端ip
def get_ip():
    if os.path.exists("/storage/emulated/0/vivoX9s"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/vivoY31s"):
        ip   ="192.168.43.123:8000"
    if os.path.exists("/storage/emulated/0/huawei20"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/oppoR9s_1d79df"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/vivoX70pro"):
        ip  ="192.168.43.123:8000"
    if os.path.exists("/storage/emulated/0/oppoA57"):
        ip  ="192.168.43.178:8000"        
    return ip
def get_device():
    device=""
    if os.path.exists("/storage/emulated/0/vivoX9s"):
        device   ="vivoX9s"
    if os.path.exists("/storage/emulated/0/oppoR9s_3881f5"):
        device   ="oppoR9s_3881f5"
    if os.path.exists("/storage/emulated/0/honor7C"):
        device   ="honor7C"
    if os.path.exists("/storage/emulated/0/oppoA57"):
        device   ="oppoA57"                
    if os.path.exists("/storage/emulated/0/oppoR9s_1d79df"):
        device   ="oppoR9s_1d79df"         
    if os.path.exists("/storage/emulated/0/oppoR9s_bfd8c5"):
        device   ="oppoR9s_bfd8c5"         
    if os.path.exists("/storage/emulated/0/oppoR9s_ae68bb"):
        device   ="oppoR9s_ae68bb"         
    if os.path.exists("/storage/emulated/0/vivoX70pro"):
        device ="vivoX70pro"
    return device
    
def tongji(click_client_ip="",click_client_device="",module="",item_id="0",visit_spend="0"):
    pass
    #print("device:",click_client_device)
    # #统计模块开始
    # conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
    # sql="insert into tongji(click_time,click_action,visit_spend,item_id,click_client_ip,click_client_device) values("+str(int(time.time()))+",'"+module+"',"+visit_spend+","+item_id+",'"+click_client_ip+"','"+click_client_device+"')"
    # result=conn.cursor().execute(sql)
    # conn.commit()
    # conn.close()
    # #统计模块结束




def execute(db_name, sql, parameters=()):
    """
    执行单条 SQL 语句（支持参数化查询）
    
    :param db_name: 数据库名（如 "organization"），对应 db/{db_name}.db
    :param sql: SQL 语句，使用 ? 作为占位符
    :param parameters: 参数元组
    :return: fetchall() 结果（如果是查询）或 None
    """
    db_path = os.path.join(BASE_DIR, "db", f"{db_name}.db")
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(sql, parameters)  # ✅ 安全的参数化查询
        if sql.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
        return result
    finally:
        conn.close()

def executes(db_name, statements):
    """
    在一个事务中执行多条参数化的 SQL 语句。
    
    :param db_name: 数据库文件名（不带 .db），如 "organization"
    :param statements: 列表，每个元素为 (sql, parameters) 元组
                       例如: [("UPDATE ...", (val1, val2)), ...]
    :raises: sqlite3.Error 如果任何语句失败，整个事务回滚
    """
    db_path = os.path.join(BASE_DIR, "db", f"{db_name}.db")
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("BEGIN")  # 显式开启事务
        cursor = conn.cursor()
        for sql, params in statements:
            cursor.execute(sql, params)  # ✅ 参数化，防注入
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()        




def find(db="",sql=""):
    try:
        conn = sqlite3.connect(os.path.join( "db", db + ".db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        resultset = cursor.fetchall()
        
        # 健壮性处理：空结果集直接返回None
        if len(resultset) == 0:
            return None  # 明确返回None而非空字典[1,9](@ref)
        
        col_name_list = [tuple[0] for tuple in cursor.description]
        return dict(zip(col_name_list, resultset[0]))
    
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return None  # 异常时返回None[2](@ref)
    
    finally:
        conn.close()  # 确保连接关闭[8](@ref)        
    
def select(db="",sql=""):
    conn=sqlite3.connect(os.path.join("db",db+".db"))
    cursor=conn.cursor()
    result=cursor.execute(sql)
    conn.commit()
    resultset= cursor.fetchall()
    conn.close()
    #print("结果集:",resultset)
    col_name_list = [tuple[0] for tuple in cursor.description]
    #print("结果集字段名:",col_name_list)
    if len(resultset)==0:
        result={col_name_list[0]:None}
        for i in range(1,len(col_name_list)):
            result[col_name_list[i]]=None
        #print("空结果集:",[result])
        return [result]
    elif len(resultset)==1:
        #print("单行结果集:",[dict(zip(col_name_list,resultset[0]))])
        return [dict(zip(col_name_list,resultset[0]))]
    else:
        result_list=[dict(zip(col_name_list,resultset[0]))]
        for i in range(1,len(resultset)):
            result_list+=[dict(zip(col_name_list,resultset[i]))]
        #print("result_list:",result_list)
        return result_list
        
    
    
    
# # 新增一个函数
# def executes(db_name, statements):
#     conn=sqlite3.connect(os.path.join(BASE_DIR,"db",db_name+".db"))
#     try:
#         conn.execute("BEGIN")
#         for stmt in statements:
#             conn.execute(stmt)
#         conn.commit()
#     except:
#         conn.rollback()
#         raise

            
        
                
            
