from telegram.client import Telegram
import os, time
import ddddocr

ocr = ddddocr.DdddOcr(beta=True)

proxy_type = {
   '@type': 'proxyTypeSocks5',  # 'proxyTypeSocks5', 'proxyTypeHttp'
}
proxy_port = 1080
proxy_server = '127.0.0.1'

an=[1] #账号数量
# 如有两个账号，则an=[1，2]，以此类推，并在下方填入多账号信息
for accn in an:
    if accn == 1: # 第一个账号
        tg = Telegram(
            api_id=f"{os.getenv('api_id')}", # 填入 api id
            api_hash=f"{os.getenv('api_hash')}", # 填入 api hash
            phone=f"{os.getenv('phone')}", # Telegram 账号
            database_encryption_key='passw0rd!',
            files_directory=f"{os.getcwd()}/sessions", # 修改储存session文件位置，防止重启后session失效
            library_path=f"{os.getcwd()}/libtdjson.so", # libtdjson 的绝对路径
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
    #         files_directory=f"{os.getcwd()}/sessions", # 修改储存session文件位置，防止重启后session失效
    #         library_path=f"{os.getcwd()}/libtdjson.so", # libtdjson 的绝对路径
    #         如需代理，请取消下方注释
    #         proxy_server=proxy_server,
    #         proxy_port=proxy_port,
    #         proxy_type=proxy_type,
    #     )

    tg.login()
    # chat id
    # 厂妹 1429576125
    # 卷毛鼠活动机器人 1723810586

    answers = []
    message = {}

    def send_checkin():
        result=tg.send_message(
            chat_id=1723810586,
            text="/checkin", # 发送签到指令
        )
        result.wait()

    def send_verification_code(update):
        global answers
        global message
        # 所有的新消息都会被监听，增加判断只监听自己感兴趣的
        if 1723810586 == update['message']['chat_id']:
            # print(update)
            message = update['message']
            # message = update['message']['content']
            print('content', message['content'])

            if (message.__contains__('reply_markup')):
                # print('reply_markup', message['reply_markup'])
                answers = message['reply_markup']['rows'][0]
                answers.extend(message['reply_markup']['rows'][1])

            if (message['content'].__contains__('photo')):
                file_id = message['content']['photo']['sizes'][0]['photo']['id']
                print('file_id', file_id)
                tg.call_method(method_name='downloadFile', params={'file_id': file_id, 'priority': 1})

            if (answers.__len__() > 0 and message['content'].__contains__('text') and message['content']['text']['text'].find('验证失败') == 0):
                send_checkin()

    def file_handler(update):
        if (update['file']['local']['is_downloading_completed']):
            file_path = update['file']['local']['path']
            print('file_path', file_path)

            with open(file_path, 'rb') as f:
                image = f.read()

            res = ocr.classification(image)
            print(f'验证码: {res}')

            if (res.__len__() != 4):
                send_checkin()
                return

            print('answers', answers)

            count = 0
            # 用答案和内联键盘值做匹配，一旦匹配执行按钮点击效果
            for x in range(len(res)):
                # print(f'目标字符：{res[x]}')
                for answer in answers:
                    # print(f'当前遍历字符：{answer["text"]}')
                    if answer['text'] == res[x]:
                        print(f'匹配目标字符：{res[x]}')
                        count += 1
                        payload = {
                            '@type': 'callbackQueryPayloadData',
                            'data': answer['type']['data'],  ##每一个内联键盘都带有data数据
                        }
                        time.sleep(1)
                        # 发送答案（点击内联键盘）
                        result = tg.call_method(method_name='getCallbackQueryAnswer',
                                                params={'chat_id': message['chat_id'],
                                                        'message_id': message['id'], 'payload': payload})
                        result.wait()
                        if result.error:
                            print(f'getCallbackQueryAnswer error: {result.error_info}')
                        else:
                            print(f'getCallbackQueryAnswer: {result.update}')
                        break

            if (count != 4):
                send_checkin()

    tg.add_update_handler('updateFile', file_handler)

    tg.add_update_handler('updateNewMessage', send_verification_code)

    result = tg.get_chats()
    result.wait()
    send_checkin()

    time.sleep(120) # 等待100秒签到完毕后退出程序
    tg.stop()
