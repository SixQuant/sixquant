# SixQuant



## 开发说明

### 单元测试
点击这个 [![Coverage report](https://img.shields.io/codecov/c/github/SixQuant/sixquant/master.svg)](https://codecov.io/github/SixQuant/sixquant?branch=master)  图标可以跳转到 https://codecov.io/github/SixQuant/sixquant 在线查看已提交代码自动构建的代码覆盖率报告，每一次 git push 都会重新生成该报告。

#### 本地安装代码覆盖率测试工具 coverage
```bash
$ pip3 install coverage
```

#### 本地执行单元测试、生成代码覆盖率报告
```bash
$ coverage run tests.py && coverage report && coverage html
```

之后打开会在 htmlcov 目录下生成报告，直接打开 [htmlcov/index.html](file:///Users/C/work/workspace/sixquant/htmlcov/index.html) 查看可视化的代码覆盖率