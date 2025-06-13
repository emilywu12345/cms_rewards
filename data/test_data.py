# test_data.py
"""
测试数据管理模块
用于集中管理自动化用例所需的测试数据，如知识库名称、描述、提示词等。
"""
import time

def get_unique_kb_name(prefix="测试知识库"):
    """
    生成唯一的知识库名称，避免重复
    """
    return f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}"

# 示例：知识库创建用例数据
def get_kb_create_data():
    return {
        "name": get_unique_kb_name(),
        "prompt": "快来创建知识库吧"
    }

# 其他测试数据可按需扩展
