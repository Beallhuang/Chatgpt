#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
from tkinter import *
import time
import openai
from memory_pic import *
import base64
import os

'''
定义消息发送函数：
1、在<消息列表分区>的文本控件中实时添加时间；
2、获取<发送消息分区>的文本内容，添加到列表分区的文本中；
3、将<发送消息分区>的文本内容清空。
'''


def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()


def main(restart_sequence):
    # print("欢迎使用ChatGPT智能问答，请在Q:后面输入你的问题，输入quit退出！")
    openai.api_key = "****"
    start_sequence = "\nA:"
    # restart_sequence = "\nQ: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # 这里我们使用的是davinci-003的模型，准确度更高。
            prompt=restart_sequence,
            temperature=1,
            max_tokens=2000,  # 这里限制的是回答的长度，你可以可以限制字数，如:写一个300字作文等。
            frequency_penalty=0,
            presence_penalty=0
        )
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     temperature=0.7,
        #     max_tokens=64,
        #     top_p=1.0,
        #     frequency_penalty=0.0,
        #     presence_penalty=0.0
        # )
        return response["choices"][0]["text"].strip()
        # print(start_sequence, response["choices"][0]["text"].strip())
    except Exception as exc:  # 捕获异常后打印出来
        print(exc)


def msgsend():
    msg = '我:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
    # print(msg)
    txt_msglist.insert(END, msg, 'green')  # 添加时间
    query = txt_msgsend.get('0.0', END)  # !!!!!!!!!!!!!!!11
    # print(query)
    result = main(query)  # 问题输入模型入口
    # print('result:', result)
    txt_msglist.insert(END, txt_msgsend.get('0.0', END))  # 获取发送消息，添加文本到消息列表
    txt_msglist.insert(END, '\n')
    txt_msgsend.delete('0.0', END)  # 清空发送消息
    robot = '小C:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n'
    txt_msglist.insert(END, robot, 'red')
    txt_msglist.insert(END, result)
    txt_msglist.insert(END, '\n\n')


'''定义取消发送 消息 函数'''


def cancel():
    txt_msgsend.delete('0.0', END)  # 取消发送消息，即清空发送消息


'''绑定up键'''


def msgsendEvent(event):
    if event.keysym == 'Return':
        msgsend()


if __name__ == '__main__':
    tk = Tk()
    tk.title('聊天工具: made by @beallhuang')
    icon_path = os.path.join(os.environ['USERPROFILE'], 'Downloads', 'icon.ico')
    get_pic(find_ico, icon_path)
    tk.iconbitmap(icon_path)
    '''创建分区'''
    f_msglist = Frame(height=300, width=300)  # 创建<消息列表分区 >
    f_msgsend = Frame(height=300, width=300)  # 创建<发送消息分区 >
    f_floor = Frame(height=100, width=300)  # 创建<按钮分区>
    f_right = Frame(height=700, width=100)  # 创建<图片分区>
    '''创建控件'''
    txt_msglist = Text(f_msglist)  # 消息列表分区中创建文本控件
    txt_msglist.tag_config('green', foreground='blue')  # 消息列表分区中创建标签
    txt_msglist.tag_config('red', foreground='red')  # 消息列表分区中创建标签
    txt_msgsend = Text(f_msgsend)  # 发送消息分区中创建文本控件

    txt_show = Text(f_msglist)  # 消息列表分区中创建文本控件
    txt_show.tag_config('red', foreground='red')  # 消息列表分区中创建标签
    txt_showsend = Text(f_msgsend)  # 发送消息分区中创建文本控件

    txt_msgsend.bind('<KeyPress-Return>', msgsendEvent)  # 发送消息分区中，绑定‘UP’键与消息发送。
    '''txt_right = Text(f_right) #图片显示分区创建文本控件'''
    button_send = Button(f_floor, text='Send', command=msgsend)  # 按钮分区中创建按钮并绑定发送消息函数
    button_cancel = Button(f_floor, text='Cancel', command=cancel)  # 分区中创建取消按钮并绑定取消函数
    '''分区布局'''
    f_msglist.grid(row=0, column=0)  # 消息列表分区
    f_msgsend.grid(row=1, column=0)  # 发送消息分区
    f_floor.grid(row=2, column=0)  # 按钮分区
    f_right.grid(row=0, column=1, rowspan=3)  # 图片显示分区
    txt_msglist.grid()  # 消息列表文本控件加载
    txt_msgsend.grid()  # 消息发送文本控件加载
    button_send.grid(row=0, column=0, sticky=W)  # 发送按钮控件加载
    button_cancel.grid(row=0, column=1, sticky=W)  # 取消按钮控件加载
    tk.mainloop()
    os.remove(icon_path)
