import time
from functools import wraps
from utils.log_manager import logger

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise
                    logger.warning(f"重试 {func.__name__} 第 {attempt} 次, 错误: {str(e)}")
                    time.sleep(delay)
        return wrapper
    return decorator