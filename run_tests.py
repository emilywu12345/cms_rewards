#!/usr/bin/env python3
"""
UI自动化测试运行脚本（优化版）
支持多种运行模式和参数配置
"""

import os
import sys
import argparse
import subprocess
import shutil
import logging
from pathlib import Path
from datetime import datetime


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        """初始化测试运行器"""
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"
        
    def setup_logging(self):
        """配置日志记录"""
        self.logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"test_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger(__name__)
        logger.info(f"日志文件创建: {log_file}")
        return logger
        
    def setup_directories(self):
        """创建必要的目录"""
        directories = [
            self.reports_dir / "allure-results",
            self.reports_dir / "allure-report", 
            self.logs_dir,
            self.project_root / "screenshots"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")
    
    def clean_old_reports(self):
        """清理旧的测试报告和相关文件"""
        print("开始清理测试环境...")
        logger = logging.getLogger(__name__)
        
        cleanup_dirs = [
            "logs",
            "screenshots", 
            "reports/allure-results",
            "reports/allure-report",
            ".pytest_cache"
        ]
        
        cleaned_count = 0
        
        for dir_path in cleanup_dirs:
            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path, ignore_errors=True)
                    cleaned_count += 1
                    logger.debug(f"清理目录: {dir_path}")
            except Exception as e:
                print(f"清理目录 {dir_path} 时出错: {str(e)}")
                logger.warning(f"清理目录 {dir_path} 时出错: {str(e)}")
        
        # 清理Python缓存
        try:
            for root, dirs, files in os.walk('.'):
                if '__pycache__' in dirs:
                    cache_dir = os.path.join(root, '__pycache__')
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    cleaned_count += 1
                    dirs.remove('__pycache__')
        except Exception as e:
            logger.warning(f"清理Python缓存时出错: {str(e)}")
        
        print(f"清理完成！共清理了 {cleaned_count} 个目录")
        logger.info(f"清理完成，共清理了 {cleaned_count} 个目录")
        print("-" * 60)
    
    def build_pytest_command(self, args):
        """构建pytest命令"""
        cmd = ["python", "-m", "pytest"]
        
        # 基本参数
        cmd.extend(["-v", "--tb=short"])
        
        # 环境和浏览器参数
        if args.env:
            cmd.extend(["--env", args.env])
        if args.browser:
            cmd.extend(["--browser", args.browser])
        if args.headless:
            cmd.extend(["--headless", "True"])
        
        # 测试控制参数
        if args.parallel:
            cmd.extend(["-n", str(args.parallel)])
        if args.markers:
            cmd.extend(["-m", args.markers])
        if args.reruns:
            cmd.extend(["--reruns", str(args.reruns)])
        if args.timeout:
            cmd.extend(["--timeout", str(args.timeout)])
        
        # Allure报告
        cmd.extend(["--alluredir", str(self.reports_dir / "allure-results")])
        
        # 测试路径
        if args.test_path:
            cmd.append(args.test_path)
        else:
            cmd.append("tests/")
        
        return cmd
    
    def run_tests(self, args):
        """运行测试"""
        logger = self.setup_logging()
        
        print("开始运行UI自动化测试")
        print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试环境: {args.env}")
        print(f"浏览器: {args.browser}")
        print(f"无头模式: {args.headless}")
        print(f"快速关闭: {args.fast_close}")
        print("-" * 60)
        
        logger.info(f"测试配置 - 环境: {args.env}, 浏览器: {args.browser}, 无头模式: {args.headless}, 快速关闭: {args.fast_close}")
        
        # 设置环境变量，传递给 conftest.py
        if args.fast_close:
            os.environ["PYTEST_FAST_CLOSE"] = "true"
        else:
            os.environ["PYTEST_FAST_CLOSE"] = "false"
        
        self.setup_directories()
        
        if args.clean:
            self.clean_old_reports()
        
        cmd = self.build_pytest_command(args)
        print(f"执行命令: {' '.join(cmd)}")
        logger.info(f"执行命令: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            logger.info("开始执行测试用例")
            result = subprocess.run(cmd, cwd=self.project_root)
            
            print("-" * 60)
            if result.returncode == 0:
                print("测试执行成功完成")
                logger.info("测试执行成功完成")
            else:
                print(f"测试执行失败，退出码: {result.returncode}")
                logger.error(f"测试执行失败，退出码: {result.returncode}")
            
            if args.allure_report:
                self.generate_allure_report()
                
            if args.open_report:
                self.open_allure_report()
                
            logger.info(f"测试完成，最终退出码: {result.returncode}")
            return result.returncode
            
        except KeyboardInterrupt:
            print("\n测试被用户中断")
            logger.warning("测试被用户中断")
            return 1
        except Exception as e:
            print(f"测试执行异常: {str(e)}")
            logger.error(f"测试执行异常: {str(e)}", exc_info=True)
            return 1
    
    def generate_allure_report(self):
        """生成Allure报告"""
        print("生成Allure报告...")
        logger = logging.getLogger(__name__)
        
        allure_results = self.reports_dir / "allure-results"
        allure_report = self.reports_dir / "allure-report"
        
        if not allure_results.exists() or not list(allure_results.glob("*")):
            print("未找到Allure测试结果，跳过报告生成")
            logger.warning("未找到Allure测试结果")
            return
        
        try:
            cmd = [
                "allure", "generate", 
                str(allure_results), 
                "-o", str(allure_report),
                "--clean"
            ]
            
            logger.info(f"执行Allure命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Allure报告生成成功: {allure_report}")
                logger.info(f"Allure报告生成成功: {allure_report}")
            else:
                print(f"Allure报告生成失败: {result.stderr}")
                logger.error(f"Allure报告生成失败: {result.stderr}")
                
        except FileNotFoundError:
            print("未安装Allure命令行工具，请先安装Allure")
            logger.error("未安装Allure命令行工具")
        except Exception as e:
            print(f"生成Allure报告异常: {str(e)}")
            logger.error(f"生成Allure报告异常: {str(e)}", exc_info=True)
    
    def open_allure_report(self):
        """打开Allure报告"""
        logger = logging.getLogger(__name__)
        allure_report = self.reports_dir / "allure-report" / "index.html"
        
        if allure_report.exists():
            try:
                if sys.platform.startswith('win'):
                    os.startfile(str(allure_report))
                elif sys.platform.startswith('darwin'):
                    subprocess.run(["open", str(allure_report)])
                else:
                    subprocess.run(["xdg-open", str(allure_report)])
                print(f"已打开Allure报告: {allure_report}")
                logger.info(f"已打开Allure报告: {allure_report}")
            except Exception as e:
                print(f"打开报告失败: {str(e)}")
                logger.error(f"打开报告失败: {str(e)}")
        else:
            print("未找到Allure报告文件")
            logger.warning("未找到Allure报告文件")
    
    def serve_allure_report(self, port=8080):
        """启动Allure报告服务"""
        logger = logging.getLogger(__name__)
        allure_results = self.reports_dir / "allure-results"
        
        if not allure_results.exists():
            print("未找到Allure测试结果")
            logger.warning("未找到Allure测试结果")
            return
        
        try:
            print(f"启动Allure报告服务，端口: {port}")
            print(f"报告地址: http://localhost:{port}")
            logger.info(f"启动Allure报告服务，端口: {port}")
            
            cmd = ["allure", "serve", str(allure_results), "-p", str(port)]
            subprocess.run(cmd)
            
        except FileNotFoundError:
            print("未安装Allure命令行工具")
            logger.error("未安装Allure命令行工具")
        except KeyboardInterrupt:
            print("\n报告服务已停止")
            logger.info("报告服务被用户停止")
        except Exception as e:
            print(f"启动报告服务异常: {str(e)}")
            logger.error(f"启动报告服务异常: {str(e)}", exc_info=True)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="UI自动化测试运行器（优化版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 运行所有测试
  python run_tests.py
  
  # 运行指定环境的冒烟测试
  python run_tests.py --env uat --markers smoke
  
  # 无头模式运行测试
  python run_tests.py --headless
  
  # 快速关闭模式运行测试（推荐，避免浏览器关闭缓慢）
  python run_tests.py --fast-close
  
  # 运行特定测试文件
  python run_tests.py --test-path tests/test_0_login.py
  
  # 生成并打开Allure报告
  python run_tests.py --allure-report --open-report
  
  # 启动Allure报告服务
  python run_tests.py --serve-report
        """
    )
    
    # 基本参数
    parser.add_argument("--env", default="uat", 
                       choices=["qa", "uat"],
                       help="测试环境 (默认: uat)")
    
    parser.add_argument("--browser", default="chrome",
                       choices=["chrome", "firefox", "edge"],
                       help="浏览器类型 (默认: chrome)")
    
    parser.add_argument("--headless", action="store_true",
                       help="启用无头模式")
    
    # 测试控制参数
    parser.add_argument("--markers", 
                       help="测试标记过滤 (如: smoke, regression)")
    
    parser.add_argument("--test-path",
                       help="指定测试文件或目录路径")
    
    parser.add_argument("--parallel", type=int,
                       help="并行执行进程数 (需要pytest-xdist)")
    
    parser.add_argument("--reruns", type=int, default=0,
                       help="失败重跑次数")
    
    parser.add_argument("--timeout", type=int,
                       help="单个测试超时时间(秒)")
    
    # 报告参数
    parser.add_argument("--allure-report", action="store_true",
                       help="生成Allure报告")
    
    parser.add_argument("--open-report", action="store_true",
                       help="自动打开Allure报告")
    
    parser.add_argument("--serve-report", action="store_true",
                       help="启动Allure报告服务")
    
    parser.add_argument("--port", type=int, default=8080,
                       help="报告服务端口 (默认: 8080)")
    
    # 其他参数
    parser.add_argument("--clean", action="store_true",
                       help="运行前清理旧报告和缓存")
    
    parser.add_argument("--fast-close", action="store_true",
                       help="启用快速关闭模式，强制终止浏览器进程避免关闭缓慢（推荐）")
    
    args = parser.parse_args()
    
    # 创建测试运行器
    runner = TestRunner()
    
    # 如果只是启动报告服务
    if args.serve_report:
        runner.serve_allure_report(args.port)
        return
    
    # 运行测试
    exit_code = runner.run_tests(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
