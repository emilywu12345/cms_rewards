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
从项目根目录运行以下命令：
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
