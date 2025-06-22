import pytest
import os
import shutil
import argparse
import logging
from datetime import datetime
from utils.config_manager import ConfigManager

def parse_args():
    """
    解析命令列參數
    """
    parser = argparse.ArgumentParser(description='Web UI自動化測試執行工具')
    parser.add_argument('--env', default='uat', choices=['qa', 'uat'],
                      help='運行環境(qa/uat)')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox'],
                      help='瀏覽器類型')
    parser.add_argument('--headless', action='store_true',
                      help='是否使用無頭模式運行')
    parser.add_argument('--cases', default='tests/',
                      help='測試用例路徑，支援特定檔案或目錄')
    parser.add_argument('--markers', 
                      help='運行指定標記的用例，如：smoke, regression')
    parser.add_argument('--reruns', type=int, default=0,
                      help='失敗用例重試次數')
    parser.add_argument('--clean', action='store_true',
                      help='是否清理歷史報告和日誌')
    return parser.parse_args()

def setup_logging():
    """
    配置日誌紀錄
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
    清理歷史檔案和目錄
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
                # 處理萬用字元模式
                import glob
                for dir_path in glob.glob(dir_pattern, recursive=True):
                    if os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        logging.info(f"已清理目錄: {dir_path}")
            else:
                # 處理具體目錄
                if os.path.exists(dir_pattern):
                    shutil.rmtree(dir_pattern)
                    logging.info(f"已清理目錄: {dir_pattern}")
        except Exception as e:
            logging.warning(f"清理目錄 {dir_pattern} 失敗: {str(e)}")

def create_dirs():
    """
    建立必要的目錄
    """
    dirs_to_create = [
        "logs",
        "screenshots",
        "reports/allure-results",
        "reports/allure-report"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"已建立目錄: {dir_path}")

def run_tests(args):
    """
    執行測試用例
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
    
    logging.info(f"開始執行測試，參數: {' '.join(pytest_args)}")
    return pytest.main(pytest_args)

def generate_report():
    """
    產生 Allure 報告
    """
    try:
        os.system("allure generate reports/allure-results -o reports/allure-report --clean")
        logging.info("已產生 Allure 報告")
        
        # 複製最新報告到固定目錄
        latest_report = "reports/allure-report/index.html"
        if os.path.exists(latest_report):
            logging.info(f"測試報告已產生: {os.path.abspath(latest_report)}")
    except Exception as e:
        logging.error(f"產生報告失敗: {str(e)}")

if __name__ == "__main__":
    # 解析命令列參數
    args = parse_args()
    
    # 設定日誌
    setup_logging()
    
    try:
        # 清理目錄（如有需要）
        if args.clean:
            clean_dirs()
        
        # 建立必要的目錄
        create_dirs()
        
        # 執行測試
        exit_code = run_tests(args)
        
        # 產生報告
        generate_report()
        
        # 結束
        exit(exit_code)
    except Exception as e:
        logging.error(f"執行測試過程中發生錯誤: {str(e)}")
        exit(1)