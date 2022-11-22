# 一键登录ecjtu校园网

byRequests.py 是用requests库实现登录的版本，更轻巧快捷。

## Usage

1. 安装依赖
```python
pip3 install -r requirements.txt
```

2. 自动认证，第一次使用需要输入学号和密码以及运营商并选择当前操作系统
```python
python3 byRequsts.py
```

3. 配置定时执行脚本，从此无需手动认证。（我是在linux软路由跑这个脚本，windows自行百度)

## update

2022-11-22: 添加定时凌晨2:30自动执行登入脚本