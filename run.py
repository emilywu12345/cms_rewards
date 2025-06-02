import pytest
import os
import shutil
import argparse
import logging
from datetime import datetime
from utils.config_loader import ConfigLoader

def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='Web UI自动化测试执行工具')
    parser.add_argument('--env', default='uat', choices=['qa', 'uat'],
                      help='运行环境(qa/uat)')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox'],
                      help='浏览器类型')
    parser.add_argument('--headless', action='store_true',
                      help='是否使用无头模式运行')
    parser.add_argument('--cases', default='tests/',
                      help='测试用例路径，支持特定文件或目录')
    parser.add_argument('--markers', 
                      help='运行指定标记的用例，如：smoke, regression')
    parser.add_argument('--reruns', type=int, default=0,
                      help='失败用例重试次数')
    parser.add_argument('--clean', action='store_true',
                      help='是否清理历史报告和日志')
    return parser.parse_args()

def setup_logging():
    """
    配置日志记录
    """
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'run_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def clean_dirs():
    """
    清理历史文件和目录
    """
    dirs_to_clean = [
        "reports",
        "screenshots",
        "logs",
        ".pytest_cache",
        "**/__pycache__"
    ]
    
    for dir_pattern in dirs_to_clean:
        try:
            if '*' in dir_pattern:
                # 处理通配符模式
                import glob
                for dir_path in glob.glob(dir_pattern, recursive=True):
                    if os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        logging.info(f"已清理目录: {dir_path}")
            else:
                # 处理具体目录
                if os.path.exists(dir_pattern):
                    shutil.rmtree(dir_pattern)
                    logging.info(f"已清理目录: {dir_pattern}")
        except Exception as e:
            logging.warning(f"清理目录 {dir_pattern} 失败: {str(e)}")

def create_dirs():
    """
    创建必要的目录
    """
    dirs_to_create = [
        "logs",
        "screenshots",
        "reports/allure-results",
        "reports/allure-report"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"已创建目录: {dir_path}")

def run_tests(args):
    """
    运行测试用例
    """
    pytest_args = [
        args.cases,
        '-v',
        f"--env={args.env}",
        f"--browser={args.browser}",
        f"--headless={'True' if args.headless else 'False'}",
        '--alluredir=reports/allure-results',
        '--clean-alluredir'
    ]
    
    if args.markers:
        pytest_args.append(f"-m {args.markers}")
    
    if args.reruns > 0:
        pytest_args.extend(['--reruns', str(args.reruns)])
    
    logging.info(f"开始执行测试，参数: {' '.join(pytest_args)}")
    return pytest.main(pytest_args)

def generate_report():
    """
    生成Allure报告
    """
    try:
        os.system("allure generate reports/allure-results -o reports/allure-report --clean")
        logging.info("已生成Allure报告")
        
        # 复制最新报告到固定目录
        latest_report = "reports/allure-report/index.html"
        if os.path.exists(latest_report):
            logging.info(f"测试报告已生成: {os.path.abspath(latest_report)}")
    except Exception as e:
        logging.error(f"生成报告失败: {str(e)}")

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志
    setup_logging()
    
    try:
        # 清理目录（如果需要）
        if args.clean:
            clean_dirs()
        
        # 创建必要的目录
        create_dirs()
        
        # 运行测试
        exit_code = run_tests(args)
        
        # 生成报告
        generate_report()
        
        # 退出
        exit(exit_code)
    except Exception as e:
        logging.error(f"执行测试过程中发生错误: {str(e)}")
        exit(1)