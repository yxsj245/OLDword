import random
import easygui
import requests
import json
import os

easygui.msgbox("1.本程序核心逻辑由chatGPT完成，部分网络请求由xxx和chatGPT共同完成。\n2.本程序需涉及后端服务器，全程需要进行联网运行,否则会出现程序崩溃.\n3.本程序在运行时会在控制台输出当前运行状态以确保遇到问题能够及时找到原因",title="注意事项")
print("开始检测新版本。如果长时间无反应可能是您的网络出现问题或服务器目前正在维护。")
url = "http://43.248.187.3:48054/version"
r = requests.get(url)
text = r.json()
if text["version"] != "1.0":
    print("检测到新版本")
    easygui.msgbox("检测到目前有新版本")
    url = "http://43.248.187.3:48147/content"
    r = requests.get(url)
    easygui.msgbox("新版本内容:\n%s"%r.text)
    xuanze = easygui.buttonbox("是否前往更新",choices=["是","否"])
    if xuanze == "是":
        easygui.msgbox("提取码：4o1b 请记住")
        print("即将跳转下载地址")
        os.popen("start https://xiaozhux.lanzouf.com/b03jytc6j")
        exit()
    else:
        print("已选择放弃本次更新")
print("没有新版本")
#每日单词的请求
def everday():
    url = "http://43.248.187.3:48139/api/everyday"
    r = requests.get(url)
    return r
#全部单词的请求
def all():
    url = "http://43.248.187.3:48151/api/all"
    r = requests.get(url)
    return r
xuanze = easygui.buttonbox("欢迎使用单词测试程序",title="主菜单",choices=["今日单词","全部单词","管理员登陆","公告","小朱API接口文档"])
if xuanze == "今日单词":
    ri = everday()
    print("以下开始进行前后端交互，过程请确保网络已连接，如果长时间无响应则代表您的网络可能出现问题或服务器正在维护")
    print("INFO：执行今日单词请求方法")
    if ri.status_code == requests.codes.ok:
        print("INFO：后端请求状态码正常")
        text = ri.text
        print("INFO：已接收到请求返回内容")
        data_dict = json.loads(text)
        print("INFO：已将JSON转换成列表")
        data_dive = data_dict['data']
        words = {}
        for word_pair in data_dive:
            word, chinese = word_pair.split('：')
            words[word] = chinese
        print("INFO：单词与汉语整理完毕，程序已准备就绪")
        easygui.msgbox("今日单词已接收完毕，状态已准备就绪。", title="背单词程序", ok_button="开始测试")
        correct_count = 0
        wrong_words = []
        # 循环等待用户输入单词，并判断是否正确
        while words:
            # 从单词字典中随机选择一个单词
            random_word = random.choice(list(words.keys()))
            # 显示随机选择的单词的汉语意思
            chinese = words[random_word]

            while True:
                word = easygui.enterbox("请输入 %s 对应的英文单词，或者点击取消退出程序：" % (chinese),
                                        title="背单词程序")
                if word is None:
                    break
                if word.lower() == random_word.lower():
                    easygui.msgbox("恭喜，您回答正确！", title="背单词程序", ok_button="下一个单词")
                    # 从单词字典中删除已经测试过的单词
                    del words[random_word]
                    correct_count += 1
                    break
                else:
                    easygui.msgbox("抱歉，您回答错误，正确答案是 %s，请再试一次。" % random_word, title="背单词程序",
                                   ok_button="重新输入")
                    wrong_words.append(random_word)

        total_count = correct_count + len(wrong_words)
        accuracy = correct_count / total_count if total_count > 0 else 0

        msg = "恭喜，您已经完成了所有单词的测试！\n\n"
        msg += "正确率为：{:.2%}\n\n".format(accuracy)
        if wrong_words:
            msg += "错误单词列表：\n" + "\n".join(wrong_words)
        easygui.msgbox(msg, title="背单词程序", ok_button="退出程序")
    else:
        print("ERROR：与后端服务器请求出现错误")
        easygui.msgbox("ERROR：与后端服务器请求出现错误，状态返回码为%s 请联系负责人" % (ri))
    # 将单词和对应汉语存储到字典中
elif xuanze == "全部单词":
    xuanze = easygui.buttonbox("请选择抽取的单词的方案",choices=["按个数随机抽取","全部随机抽取"])
    if xuanze == "全部随机抽取":
        print("以下开始进行前后端交互，过程请确保网络已连接，如果长时间无响应则代表您的网络可能出现问题或服务器正在维护")
        ri = all()
        print("INFO：执行今日单词请求方法")
        if ri.status_code == requests.codes.ok:
            print("INFO：后端请求状态码正常")
            text = ri.text
            print("INFO：已接收到请求返回内容")
            data_dict = json.loads(text)
            print("INFO：已将JSON转换成列表")
            data_dive = data_dict['data']
            words = {}
            for word_pair in data_dive:
                word, chinese = word_pair.split('：')
                words[word] = chinese
            print("INFO：单词与汉语整理完毕，程序已准备就绪")
            print(len(words))
            easygui.msgbox("今日单词已接收完毕，状态已准备就绪。", title="背单词程序", ok_button="开始测试")
            correct_count = 0
            wrong_words = []

            # 循环等待用户输入单词，并判断是否正确
            while words:
                # 从单词字典中随机选择一个单词
                random_word = random.choice(list(words.keys()))
                # 显示随机选择的单词的汉语意思
                chinese = words[random_word]

                while True:
                    word = easygui.enterbox("请输入 %s 对应的英文单词，或者点击取消退出程序：" % (chinese),
                                            title="背单词程序")
                    if word is None:
                        break
                    if word.lower() == random_word.lower():
                        easygui.msgbox("恭喜，您回答正确！", title="背单词程序", ok_button="下一个单词")
                        # 从单词字典中删除已经测试过的单词
                        del words[random_word]
                        correct_count += 1
                        break
                    else:
                        easygui.msgbox("抱歉，您回答错误，正确答案是 %s，请再试一次。" % random_word, title="背单词程序",
                                       ok_button="重新输入")
                        wrong_words.append(random_word)

            total_count = correct_count + len(wrong_words)
            accuracy = correct_count / total_count if total_count > 0 else 0

            msg = "恭喜，您已经完成了所有单词的测试！\n\n"
            msg += "正确率为：{:.2%}\n\n".format(accuracy)
            if wrong_words:
                msg += "错误单词列表：\n" + "\n".join(wrong_words)
            easygui.msgbox(msg, title="背单词程序", ok_button="退出程序")
        else:
            print("ERROR：与后端服务器请求出现错误")
            easygui.msgbox("ERROR：与后端服务器请求出现错误，状态返回码为%s 请联系负责人" % (ri))
    else:
        print("以下开始进行前后端交互，过程请确保网络已连接，如果长时间无响应则代表您的网络可能出现问题或服务器正在维护")
        ri = all()
        print("INFO：执行获取全部单词请求方法")
        if ri.status_code == requests.codes.ok:
            print("INFO：后端请求状态码正常")
            text = ri.text
            print("INFO：已接收到请求返回内容")
            data_dict = json.loads(text)
            print("INFO：已将JSON转换成列表")
            data_dive = data_dict['data']
            words = {}
            for word_pair in data_dive:
                word, chinese = word_pair.split('：')
                words[word] = chinese
            print("INFO：单词与汉语整理完毕，程序已准备就绪")
            print()
            shuru = easygui.integerbox("请输入抽取的单词个数，最大不能超过%s个"%len(words),lowerbound=1,upperbound=len(words))
            easygui.msgbox("今日单词已接收完毕，状态已准备就绪。", title="背单词程序", ok_button="开始测试")
            correct_count = 0
            wrong_words = []

            # 循环等待用户输入单词，并判断是否正确
            for i in range(shuru):
                # 从单词字典中随机选择一个单词
                random_word = random.choice(list(words.keys()))
                # 显示随机选择的单词的汉语意思
                chinese = words[random_word]

                while True:
                    word = easygui.enterbox("请输入 %s 对应的英文单词，或者点击取消退出程序：" % (chinese),
                                            title="背单词程序")
                    if word is None:
                        break
                    if word.lower() == random_word.lower():
                        easygui.msgbox("恭喜，您回答正确！", title="背单词程序", ok_button="下一个单词")
                        # 从单词字典中删除已经测试过的单词
                        del words[random_word]
                        correct_count += 1
                        break
                    else:
                        easygui.msgbox("抱歉，您回答错误，正确答案是 %s，请再试一次。" % random_word, title="背单词程序",
                                       ok_button="重新输入")
                        wrong_words.append(random_word)

            total_count = correct_count + len(wrong_words)
            accuracy = correct_count / total_count if total_count > 0 else 0

            msg = "恭喜，您已经完成了所有单词的测试！\n\n"
            msg += "正确率为：{:.2%}\n\n".format(accuracy)
            if wrong_words:
                msg += "错误单词列表：\n" + "\n".join(wrong_words)
            easygui.msgbox(msg, title="背单词程序", ok_button="退出程序")
        else:
            print("ERROR：与后端服务器请求出现错误")
            easygui.msgbox("ERROR：与后端服务器请求出现错误，状态返回码为%s 请联系负责人" % (ri))
elif xuanze == "管理员登陆":
    url = 'http://43.248.187.3:5000/login'
    data = {'username': 'alice', 'password': 'secret'}
    data["username"] = easygui.enterbox("请输入账号")
    data["password"] = easygui.passwordbox("请输入密码")
    print("准备提交登陆信息")
    response = requests.post(url, json=data)
    print(response.json())
    response = response.json()
    print("服务器响应完成")
    if response["message"] == "Login successful":
        print("登陆成功")
        easygui.buttonbox("欢迎登陆后台管理员系统")
    else:
        print("登陆失败")
        easygui.msgbox("登陆出现错误，错误返回内容：%s"%(response))
elif xuanze == "小朱API接口文档":
    os.popen("start https://xz-kun-xiang.com:48143/forums/%E5%B0%8F%E6%9C%B1api%E5%85%AC%E5%BC%80%E6%8E%A5%E5%8F%A3.14/")
elif xuanze == "公告":
    url = "http://43.248.187.3:48080/state"
    r = requests.get(url)
    easygui.msgbox(r.text,title="公告")
