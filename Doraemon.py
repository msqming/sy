#!/usr/bin/python
# -*- coding:utf-8 -*-

# from turtle import *
import turtle as t


# 无轨迹跳跃
def my_goto(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


# 眼睛
def eyes():
    t.tracer(False)
    a = 2.5
    for i in range(120):
        if 0 <= i < 30 or 60 <= i < 90:
            a -= 0.05
            t.lt(3)
            t.fd(a)
        else:
            a += 0.05
            t.lt(3)
            t.fd(a)
    t.tracer(True)


# 胡须
def beard():
    my_goto(-37, 135)
    t.seth(165)
    t.fd(60)
    my_goto(-37, 125)
    t.seth(180)
    t.fd(60)
    my_goto(-37, 115)
    t.seth(193)
    t.fd(60)
    my_goto(37, 135)
    t.seth(15)
    t.fd(60)
    my_goto(37, 125)
    t.seth(0)
    t.fd(60)
    my_goto(37, 115)
    t.seth(-13)
    t.fd(60)


# 嘴巴
def mouth():
    my_goto(5, 148)
    t.seth(270)
    t.fd(100)
    t.seth(0)
    t.circle(120, 50)
    t.seth(230)
    t.circle(-120, 100)


# 围巾
def scarf():
    t.fillcolor('#e70010')
    t.begin_fill()
    t.seth(0)
    t.fd(200)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.fd(207)
    t.circle(-5, 90)
    t.fd(10)
    t.circle(-5, 90)
    t.end_fill()


# 鼻子
def nose():
    my_goto(-10, 158)
    t.fillcolor('#e70010')
    t.begin_fill()
    t.circle(20)
    t.end_fill()


# 黑眼睛
def black_eyes():
    t.seth(0)
    my_goto(-20,195)
    t.fillcolor('#000000')
    t.begin_fill()
    t.circle(13)
    t.end_fill()
    t.pensize(6)
    my_goto(20,205)
    t.seth(75)
    t.circle(-17,200)
    t.seth(0)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    my_goto(0,0)


# 脸
def face():
    t.fd(183)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.lt(45)
    t.circle(120,100)
    t.seth(90)
    eyes()
    t.seth(180)
    t.penup()
    t.fd(60)
    t.pendown()
    t.seth(90)
    eyes()
    t.penup()
    t.seth(180)
    t.fd(64)
    t.pendown()
    t.seth(215)
    t.circle(120,100)
    t.end_fill()


# 头型
def head():
    t.penup()
    t.circle(150,40)
    t.pendown()
    t.fillcolor('#00a0de')
    t.begin_fill()
    t.circle(150,280)
    t.end_fill()


# 画哆啦A梦
def Doraemon():
    # 头部
    head()
    # 围脖
    scarf()
    # 脸
    face()
    # 红鼻子
    nose()
    # 嘴巴
    mouth()
    # 胡须
    beard()
    # 身体
    my_goto(0, 0)
    t.seth(0)
    t.penup()
    t.circle(150, 50)
    t.pendown()
    t.seth(30)
    t.fd(40)
    t.seth(70)
    t.circle(-30, 270)
    t.fillcolor('#00a0de')
    t.begin_fill()
    t.seth(230)
    t.fd(80)
    t.seth(90)
    t.circle(1000, 1)
    t.seth(-89)
    t.circle(-1000, 10)
    # print(pos())
    t.seth(180)
    t.fd(70)
    t.seth(90)
    t.circle(30, 180)
    t.seth(180)
    t.fd(70)
    # print(pos())
    t.seth(100)
    t.circle(-1000, 9)
    t.seth(-86)
    t.circle(1000, 2)
    t.seth(230)
    t.fd(40)
    # print(pos())
    t.circle(-30, 230)
    t.seth(45)
    t.fd(81)
    t.seth(0)
    t.fd(203)
    t.circle(5, 90)
    t.fd(10)
    t.circle(5, 90)
    t.fd(7)
    t.seth(40)
    t.circle(150, 10)
    t.seth(30)
    t.fd(40)
    t.end_fill()

    # 左手
    t.seth(70)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.circle(-30)
    t.end_fill()

    # 脚
    my_goto(103.74, -182.59)
    t.seth(0)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.fd(15)
    t.circle(-15, 180)
    t.fd(90)
    t.circle(-15, 180)
    t.fd(10)
    t.end_fill()
    my_goto(-96.26, -182.59)
    t.seth(180)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.fd(15)
    t.circle(15, 180)
    t.fd(90)
    t.circle(15, 180)
    t.fd(10)
    t.end_fill()

    # 右手
    my_goto(-133.97, -91.81)
    t.seth(50)
    t.fillcolor('#ffffff')
    t.begin_fill()
    t.circle(30)
    t.end_fill()

    # 口袋
    my_goto(-103.42, 15.09)
    t.seth(0)
    t.fd(38)
    t.seth(230)
    t.begin_fill()
    t.circle(90, 260)
    t.end_fill()
    my_goto(5, -40)
    t.seth(0)
    t.fd(70)
    t.seth(-90)
    t.circle(-70, 180)
    t.seth(0)
    t.fd(70)
    #铃铛
    my_goto(-103.42, 15.09)
    t.fd(90)
    t.seth(70)
    t.fillcolor('#ffd200')
    # print(pos())
    t.begin_fill()
    t.circle(-20)
    t.end_fill()
    t.seth(170)
    t.fillcolor('#ffd200')
    t.begin_fill()
    t.circle(-2, 180)
    t.seth(10)
    t.circle(-100, 22)
    t.circle(-2, 180)
    t.seth(180-10)
    t.circle(100, 22)
    t.end_fill()
    t.goto(-13.42, 15.09)
    t.seth(250)
    t.circle(20, 110)
    t.seth(90)
    t.fd(15)
    t.dot(10)
    my_goto(0, -150)
    # 画眼睛
    black_eyes()


if __name__ == '__main__':
    t.screensize(800,600, "#f0f0f0")
    t.pensize(3)  # 画笔宽度
    t.speed(9)    # 画笔速度
    Doraemon()
    my_goto(100, -300)
    t.write('by YPP', font=("Bradley Hand ITC", 30, "bold"))
    t.mainloop()