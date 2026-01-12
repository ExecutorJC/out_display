import os
import sys

"""用于处理资源文件路径的工具模块"""

def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包环境"""
    try:
        # PyInstaller创建临时文件夹的路径
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下的路径
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)