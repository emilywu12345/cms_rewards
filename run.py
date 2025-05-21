import pytest
import os
import shutil
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='UI自动化测试')
    parser.add_argument('--env', default='qa', help='运行环境(qa/stage/prod)')
    parser.add_argument('--browser', default='chrome', help='浏览器类型')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    return parser.parse_args()

def init_dirs():
    # 创建时间戳目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join("reports", timestamp)
    
    # 创建必要目录
    for folder in ["logs", "screenshots", "reports"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    return report_dir

if __name__ == "__main__":
    args = parse_args()
    report_dir = init_dirs()
    
    # 执行测试
    pytest.main([
        "-v",
        f"--env={args.env}",
        f"--browser={args.browser}",
        f"--headless={args.headless}",
        f"--alluredir={report_dir}",
        "--clean-alluredir",
        "testcases/",
        "--color=yes"
    ])
    
    # 生成HTML报告
    os.system(f"allure generate {report_dir} -o {report_dir}/html --clean")
    print(f"测试报告已生成：{report_dir}/html/index.html")