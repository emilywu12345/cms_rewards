import time
from functools import wraps
from utils.log_manager import logger

# 装饰器：为函数增加失败重试机制
# 用法：@retry_on_failure(retries=3, delay=2)
# retries: 最大重试次数，delay: 每次重试间隔秒数
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise  # 最后一次失败则抛出异常
                    logger.warning(f"重试 {func.__name__} 第 {attempt} 次, 错误: {str(e)}")
                    time.sleep(delay)
        return wrapper
    return decorator