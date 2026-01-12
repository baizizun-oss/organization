#config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_ROOT = os.getenv("STORAGE_ROOT", os.path.join(BASE_DIR, "upload")) #此为organization和organization_admin共同使用的上传目录
organization_PATH = os.getenv("organization_PATH", os.path.join(BASE_DIR, "organization"))
organization_ADMIN_PATH = os.getenv("organization_ADMIN_PATH", os.path.join(BASE_DIR, "organization_admin"))

PATH = {
    # "organization": {
    #     "Works": {
    #         "js": os.path.join(BASE_DIR, "organization", "templates", "Works", "static", "js"),
    #         "css": os.path.join(BASE_DIR, "organization", "templates", "Works", "static", "css"),
    #         "images":{
    #             "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "images"),
    #             "single_choice": os.path.join(UPLOAD_ROOT, "Works", "single_choice", "images"),
    #             "multiple_choice": os.path.join(UPLOAD_ROOT, "Works", "multiple_choice", "images"),
    #             "fill_blank": os.path.join(UPLOAD_ROOT, "Works", "fill_blank", "images"),
    #             "true_false": os.path.join(UPLOAD_ROOT, "Works", "true_false", "images"),
    #         },
    #         "files":{
    #             "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "files"),
    #         },
    #         "video":{
    #             "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "video"),
    #         }            
    #     },
    #     "Answer": {
    #         "js": os.path.join(BASE_DIR, "jobs", "recordings"),
    #         "css": os.path.join(BASE_DIR, "organization", "templates", "Answer", "static", "css"),
    #         "images":{
    #             "operation": os.path.join(UPLOAD_ROOT, "Answer", "operation", "images"),
    #             "single_choice": os.path.join(UPLOAD_ROOT, "Works", "single_choice", "images"),
    #             "multiple_choice": os.path.join(UPLOAD_ROOT, "Works", "multiple_choice", "images"),
    #             "fill_blank": os.path.join(UPLOAD_ROOT, "Works", "fill_blank", "images"),
    #             "true_false": os.path.join(UPLOAD_ROOT, "Works", "true_false", "images"),
    #         },
    #         "files": os.path.join(UPLOAD_ROOT, "Answer", "files"),
    #     }        
    # },
    # "jobs": {
    #     "recordings": os.path.join(BASE_DIR, "jobs", "recordings")
    # },
    # "sangao": {  # 新增sangao配置，用于题库图片资源
    #     "Question": {
    #         "images": {
    #             "single_choice": os.path.join(UPLOAD_ROOT, "Question", "images", "single_choice"),
    #             "multiple_choice": os.path.join(UPLOAD_ROOT, "Question", "images", "multiple_choice"),
    #             "fill_blank": os.path.join(UPLOAD_ROOT, "Question", "images", "fill_blank")
    #         }
    #     }
    # },    
    "organization": {
        # "Works": {
        #     "files":{
        #         "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "files"),
        #     },
        #     "images":{
        #         "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "images"),
        #         "single_choice": os.path.join(UPLOAD_ROOT, "Works", "single_choice", "images"),
        #         "multiple_choice": os.path.join(UPLOAD_ROOT, "Works", "multiple_choice", "images"),
        #         "fill_blank": os.path.join(UPLOAD_ROOT,"Works", "fill_blank", "images")
        #     },
        #     "video":{
        #         "operation": os.path.join(UPLOAD_ROOT, "Works", "operation", "video"),
        #     }                        
        # },
        "TeachExam": {
            "js": os.path.join(BASE_DIR, "organization_admin", "templates", "TeachExam", "static", "js"),
            "images": {
                "board": os.path.join(organization_ADMIN_PATH, "upload", "TeachExam", "images", "board"),
            }
        },
        

    }
}

def get_path(*keys):
    """
    从 PATH 中根据任意深度的键路径获取绝对路径。
    
    参数:
        *keys: 路径键序列，对应 PATH 的嵌套层级
        
    示例:
        get_path("organization", "templates", "Works", "static", "js")
        get_path("organization", "upload", "Works", "operation", "files")
        get_path("organization_admin", "templates", "Works", "static", "css")
    """
    if not keys:
        raise ValueError("至少需要一个路径键")
    
    current = PATH
    path_so_far = []
    
    for i, key in enumerate(keys):
        path_so_far.append(key)
        if not isinstance(current, dict):
            raise TypeError(
                f"在路径 {' -> '.join(path_so_far[:-1])} 处期望 dict，但得到 {type(current).__name__}"
            )
        if key not in current:
            available = list(current.keys()) if isinstance(current, dict) else []
            raise KeyError(
                f"键 '{key}' 不存在于路径 {' -> '.join(path_so_far[:-1]) or '根'}。可用键: {available}"
            )
        current = current[key]
    
    if not isinstance(current, str):
        raise TypeError(
            f"最终值必须是字符串路径，但在路径 {' -> '.join(keys)} 得到 {type(current).__name__}: {current}"
        )
    
    return current


def _collect_leaf_paths(obj):
    """递归收集所有叶子节点（字符串路径）"""
    if isinstance(obj, str):
        return [obj]
    elif isinstance(obj, dict):
        paths = []
        for value in obj.values():
            paths.extend(_collect_leaf_paths(value))
        return paths
    return []


def init_storage_dirs():
    """初始化所有存储目录（仅针对 upload 类路径，但这里简单全量创建）"""
    all_paths = _collect_leaf_paths(PATH)
    for path in all_paths:
        # 可选：只创建 upload 相关目录（避免创建 templates/static 等非上传目录）
        # 但 os.makedirs(exist_ok=True) 是安全的
        os.makedirs(path, exist_ok=True)
        print(f"📁 确保目录存在: {path}")


# 初始化
init_storage_dirs()

# 使用示例
if __name__ == "__main__":
    js_path = get_path("organization", "templates", "Works", "static", "js")
    op_images = get_path("organization", "upload", "Works", "fill_blank", "images")
    admin_css = get_path("organization_admin", "templates", "Works", "static", "css")
    print("JS Path:", js_path)
    print("Fill-blank images:", op_images)
    print("Admin CSS:", admin_css)