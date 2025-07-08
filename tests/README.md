# 测试目录说明

## 配置文件
所有的测试配置（包括 fixtures、钩子函数等）都统一在项目根目录的 `conftest.py` 中管理。

## 目录结构
```
tests/
├── test_cases/              # 按功能模块组织的测试用例
│   ├── authentication/      # 认证相关测试
│   └── knowledge_base/      # 知识库相关测试
├── test_0_login.py         # 登录相关测试
└── test_1_knowledge_base.py # 知识库相关测试
```

## 运行测试

### 方式1: 使用推荐的测试运行器 (推荐)
从项目根目录运行以下命令：
```bash
# 运行所有测试 (推荐方式)
python run_tests.py

# 运行指定环境的冒烟测试
python run_tests.py --env uat --markers smoke

# 无头模式并行运行测试
python run_tests.py --headless --parallel 4

# 运行特定测试文件并生成报告
python run_tests.py --test-path tests/test_login.py --allure-report --open-report

# 查看完整参数说明
python run_tests.py --help
```

### 方式2: 直接使用pytest
```bash
# 运行所有测试
pytest

# 运行特定模块的测试
pytest tests/test_cases/authentication/

# 运行特定环境的测试
pytest --env=uat

# 生成测试报告
pytest --alluredir=reports/allure-results
```

推荐使用 `run_tests.py` 脚本，它提供了更完整的功能和更好的用户体验。
