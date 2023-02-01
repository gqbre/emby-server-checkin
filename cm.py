# Terminus终点站签到脚本
from telegram.client import Telegram
import os, time
import ddddocr

ocr = ddddocr.DdddOcr(beta=True)

proxy_type = {
   '@type': 'proxyTypeSocks5',  # 'proxyTypeSocks5', 'proxyTypeHttp'
}
proxy_port = 1080
proxy_server = '127.0.0.1'

an=[1]
# 如有两个账号，则an=[1，2]，以此类推，并在下方填入多账号信息
for accn in an:
    if accn == 1: # 第一个账号
        tg = Telegram(
            api_id=f"{os.getenv('api_id')}", # 填入 api id
            api_hash=f"{os.getenv('api_hash')}", # 填入 api hash
            phone=f"{os.getenv('phone')}", # Telegram账号
            database_encryption_key='passw0rd!',
            files_directory=f"{os.getcwd()}/sessions", # 修改储存session文件位置，防止重启后session失效
            library_path=f"{os.getcwd()}/libtdjson.so", # tdlib 的绝对路径
            # 如需代理，请取消下方注释
            # proxy_server=proxy_server,
            # proxy_port=proxy_port,
            # proxy_type=proxy_type,
        )
    # #多账号支持
    # if accn == 2:
    #     tg = Telegram(
    #         api_id='your api id', # 填入api id
    #         api_hash='your api hash', # 填入 api hash
    #         phone='your phone number', # Telegram账号
    #         database_encryption_key='passw0rd!',
    #         files_directory="/home/$(id -un)/emby-server-checkin-bot/sessions", # 修改储存session文件位置，防止重启后session失效
    #         library_path="/home/$(id -un)/emby-server-checkin-bot/libtdjson.so", # tdlib 的绝对路径
    #         如需代理，请取消下方注释
    #         proxy_server=proxy_server,
    #         proxy_port=proxy_port,
    #         proxy_type=proxy_type,
    #     )
    tg.login()
    # chat id
    # 厂妹 1429576125
    # 卷毛鼠活动机器人 1723810586

    def send_verification_code(update):
        # print('message', update)
        # 所有的新消息都会被监听，增加判断只监听自己感兴趣的
        if 1429576125 == update['message']['chat_id']:
            # print(update)
            message = update['message']['content']
            print('message', message)

            if (message.__contains__('photo')):
                file_id = message['photo']['sizes'][0]['photo']['id']
                print('file_id', file_id)
                tg.call_method(method_name='downloadFile', params={'file_id': file_id, 'priority': 1})


    def file_handler(update):
        if (update['file']['local']['is_downloading_completed']):
            file_path = update['file']['local']['path']
            print('file_path', file_path)

            with open(file_path, 'rb') as f:
                image = f.read()

            res = ocr.classification(image)
            print(f'验证码: {res}')

            time.sleep(2)

            tg.send_message(
                chat_id=1429576125,
                text=res, # 发送验证码
            )

    tg.add_update_handler('updateFile', file_handler)

    tg.add_update_handler('updateNewMessage', send_verification_code)

    result = tg.get_chats()
    result.wait()
    result = tg.send_message(
            chat_id=1429576125,
            text="/checkin", # 发送签到指令
        )
    result.wait()
    time.sleep(15) # 等待15秒签到完毕后退出程序
    tg.stop()
