# emby-server-checkin-bot
# 终点站、卷毛鼠emby公益服签到机器人
参考[Orzlee telegram-自动签到](https://www.orzlee.com/Just-write-something/2022/01/05/telegram-automatic-checkin.html)，利用[python-telegram](https://github.com/alexander-akhmetov/python-telegram)库实现

## 0x00 系统环境准备
在Ubuntu 20.04 LTS上测试成功，其余环境自行测试。

从GitHub clone 本repo:
```
cd ~
git clone https://github.com/elecxwr/emby-server-checkin-bot.git
```
## 0x01 Python环境
检查所装Python版本
```
python3 -V
```
输出应为
```
Python 3.8.2
```
否则自行安装python3.6+

安装 pip 以及虚拟环境
```
sudo apt install -y python3-pip
sudo apt install -y python3-venv
```
创建虚拟环境
```
cd emby-server-checkin-bot
python3 -m venv my_env
```
进入虚拟环境
```
source my_env/bin/activate
```
安装 python-telegram 以及打包所用 pyinstaller
```
pip install python-telegram pyinstaller
```

## 0x02 Telegram账号登陆
首先前往[Telegram官网](https://my.telegram.org)申请Application API。登陆后选择API development tools，自行填写信息后提交后即可获取 api_id 和 api_hash。若显示error可能为代理问题，更换代理后尝试。

cm.py为Terminus终点站签到脚本，jms.py为卷毛鼠公益服签到脚本，libtdjson.so为编译好的 [tdlib](https://github.com/tdlib/td) 文件。根据需求自行选择脚本进行编辑，两者编辑方式相同，以下以cm.py为例。

编辑cm.py脚本输入上一步获取的api_id 和 api_hash。支持多账号，多账号配置根据脚本中提示自行配置。
```
nano cm.py
```
自行替换脚本以下章节中api_id, api_hash, Phone number。
```python
tg = Telegram(
    api_id='your api id', # 填入api id
    api_hash='your api hash', # 填入 api hash
    phone='your phone number', # Telegram账号
    ...
)
```
编辑后保存退出。
## 0x03 运行脚本签到
运行脚本，第一次登陆需要输入两步验证码，根据提示输入。
```
python3 cm.py
```
约15s后脚本自动退出，检查Telegram中应自动签到成功。
## 0x04 打包并定时执行
签到成功后用以下命令打包方便定时执行：
```
pyinstaller -F cm.py
```
打包成功后运行dist/cm测试是否工作正常
```
dist/cm
```
工作正常后将该程序加入cron定时执行
```
crontab -e
```
在末行输入
```
1 16 * * * /home/$(id -un)/emby-server-checkin-bot/dist/cm
```
保存退出后自动签到程序将在 UTC+8 的 0:01 分自动签到



