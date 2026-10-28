#!/bin/env python
# -*-coding:utf8-*-
# 以上是使用中文的utf8编码                                                                                

import pyodbc    # 使用odbc连接数据库
import time      # 使用时间
import os        # os模块包含了操作系统有关的函数
import sys
import random
import re
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django  import forms
from django.db import connection
from datetime import datetime
from typing import List
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

global code
global pnum
global mname
global singer
global num
global allow
global yzmz
allow = 0

class BorrowInfo(object):  
    def __init__(self,mname,singer,tpnum):
        self.mname=mname
        self.singer=singer
        self.tpnum=tpnum

class ssmInFo(object):  
    def __init__(self,mname0,singer0,tpnum0):
        self.mname0=mname0
        self.singer0=singer0
        self.tpnum0=tpnum0

class ssuInFo(object):  
    def __init__(self,uname,pwdu,tpn,tgn,ph):
        self.uname=uname
        self.pwdu=pwdu
        self.tpn=tpn
        self.tgn=tgn
        self.ph=ph

class Sample:
    global pnum
    global code
    
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            access_key_id=os.environ.get("ALIYUN_ACCESS_KEY_ID", ""),
            access_key_secret=os.environ.get("ALIYUN_ACCESS_KEY_SECRET", "")
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='FTCD工作室',
            template_code='	SMS_472415118',
            phone_numbers=pnum,
            template_param=f'{{"code":"{code}"}}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.send_sms_with_options(send_sms_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='FTCD工作室',
            template_code='	SMS_472415118',
            phone_numbers=pnum,
            template_param=f'{{"code":"{code}"}}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_sms_with_options_async(send_sms_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


def is_valid_phone_number(phone_number):
    # 中国大陆手机号码正则表达式
    pattern = re.compile(r'^1[3-9]\d{9}$')
    if pattern.match(phone_number):
        return 1
    else:
        return 0

def access(request):
    phonew = request.session.get('phonew')
    if phonew:
        pass
    else:
        return HttpResponseRedirect("/accessph")
    
    if request.method =='POST':
        user=request.POST.get('txtuser')
        pwd=str(request.POST.get('txtpwd'))
        pwd2=str(request.POST.get('txtpwd2'))

        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()
            cursor.execute(u"""SELECT * FROM [users] WHERE [用户名] = ?""", user)
            namer = cursor.fetchone()
            if namer:
                warn = u"此用户名已存在！"
            else:
                if pwd == pwd2:
                    tpcs=int(4)
                    tgcs=int(1)
                    DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
                    conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
                    cursor = conn.cursor()
                    cursor.execute(u"""SELECT * FROM [users] WHERE [手机号] = ?""", phonew)
                    phonea = cursor.fetchone()
                    if phonea:
                        warn = u"请勿重复注册！"
                    else:
                        sql = u"""INSERT INTO [users]([用户名],[密码],[投票次数],[投稿次数],[手机号]) VALUES (?, ?, ?, ?, ?)"""
                        cursor.execute(sql, user, pwd, tpcs, tgcs, phonew)
                        cz = "注册"
                        yh = user
                        sj = datetime.now()
                        xx = request.META.get('REMOTE_ADDR')
                        sql = u"""INSERT INTO [command]([操作],[用户],[时间],[信息]) VALUES (?, ?, ?, ?)"""
                        cursor.execute(sql,cz,yh,sj,xx)
                        warn = u"注册成功！"
                        request.session['user'] = user
                        request.session['phone']=''
                        request.session['phonew']=''
                        request.session['yzmd']=''
                        return HttpResponseRedirect("/musictg")
                else:
                    warn = u"两次输入的密码不一致，请重新输入！"
        except Exception as e:
            warn = u"ERROR：请联系服务器管理员！"
            print(e)
 
        cursor.close()
        conn.close()
        return render(request,'access.html',{'warn':warn,'user':user} )    
    else :      
        return render(request, 'access.html')

def accessph(request):
    try:
        phone = request.session.get('phone')
        if phone:
            return HttpResponseRedirect("/accessph2")
    except:
        pass
    global pnum
    global code
    try:
        if request.method =='POST':
            phone=request.POST.get('phone')
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()
            cursor.execute(u"""SELECT * FROM [users] WHERE [手机号] = ?""", phone)
            czphone = cursor.fetchone()
            if czphone:
                warn = u"此手机号已注册！"
                return render(request,'accessph.html',{'warn':warn} )
            else:
                if phone:
                    if is_valid_phone_number(phone) == 1:
                        yzmz = random.randint(100000, 999999)
                        code = yzmz
                        pnum = phone
                        Sample.main(sys.argv[1:])
                        warn = u"已发送！"
                        request.session['phone']=phone
                        request.session['yzmd']=yzmz
                        return HttpResponseRedirect("/accessph2")
                    else:
                        warn = u"手机号格式错误！"
                else:
                     warn = u"手机号不能为空！" 
                return render(request,'accessph.html',{'warn':warn} )
        else :      
            return render(request, 'accessph.html')
    except:
        warn = u"请填写正确的手机号！"
        return render(request,'accessph.html',{'warn':warn} )
    
def accessph2(request):
    phone = request.session.get('phone')
    if phone:
        pass
    else:
        return HttpResponseRedirect("/accessph")
    
    try:    
        if request.method =='POST':
            if 'wc' in request.POST:
                yzmd = int(request.session.get('yzmd'))
                yzm = int(request.POST.get('yzm'))
                if yzm == yzmd:
                    request.session['phonew']=phone
                    return HttpResponseRedirect("/access") 
                else:
                    warn = u"验证码错误！"  
                    return render(request,'accessph2.html',{'warn':warn} )      
            if 're' in request.POST:   
                request.session['phone']=''
                request.session['phonew']=''
                request.session['yzmd']=''
                return HttpResponseRedirect("/accessph") 
            return render(request,'accessph2.html',{'warn':warn} )    
        else :      
            return render(request, 'accessph2.html')
    except:
        warn = u"请填写正确的验证码！"
        return render(request,'accessph2.html',{'warn':warn} )

def login(request):
    if request.method == 'POST':
        user = request.POST.get('txtuser')
        pwd = request.POST.get('txtpwd')
        warn = ''
        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()                            # 用游标方式
            cursor.execute(u""" Select * FROM [users] where [用户名]=?""", user)
            list=cursor.fetchall()                            # 得到查询结果
  
            if list :                                         # 查询结果有内容
                for row in list :                             # 循环遍历                
                    if row[1]==pwd:                     # 查询于结果中密码等输入的密码
                        request.session['user']=user  # 设置session
                        cz = "登录"
                        yh = user
                        sj = datetime.now()
                        xx = request.META.get('REMOTE_ADDR')
                        sql = u"""INSERT INTO [command]([操作],[用户],[时间],[信息]) VALUES (?, ?, ?, ?)"""
                        cursor.execute(sql,cz,yh,sj,xx)
                        return HttpResponseRedirect("/musictg")
                    else :
                        warn= u"用户不存在或密码错误！"
            else :
                warn = u"用户不存在或密码错误！"

        except Exception as e:
            warn= u"ERROR：请联系服务器管理员！"
            print(e)

        return render(request,'login.html',{'warn':warn,'user':user} )
    else:
        return render(request, 'login.html') 


def musictg(request):
    user = request.session.get('user', '没有用户')  # 获取session的值，没有时为'没有用户'
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 显示当前日期时间.如格式为：年-月-日 时：分：秒strftime('%Y-%m-%d %H:%M:%S')
    DBfile = os.getcwd() + u"""\数据库ftcd.mdb"""  # 起始执行目录\数据库文件
    conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
    cursor = conn.cursor()
    sql=u""" Select * FROM [musictg] order by [投票] desc"""
    cursor.execute(sql)
    list=cursor.fetchall()
    music_list=[]
    for row in list :                                       # 循环遍历
        music=BorrowInfo(row[0],row[1],row[2])
        music_list.append(music)

    if request.method == 'POST':  # post方法
        global mname
        global singer
        global num
        sql=u""" Select * FROM [musictg] order by [投票] desc"""
        cursor.execute(sql)
        list=cursor.fetchall()
        music_list=[]
        for row in list :                                       # 循环遍历
            music=BorrowInfo(row[0],row[1],row[2])
            music_list.append(music)                              # 将对象添加到传递到页面设计的列表
 
        if 'sx' in request.POST:
            warn= u"刷新列表成功！"
            sql=u""" Select * FROM [musictg] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            music_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                music_list.append(music)
            return render(request,'musictg.html',{'music_list':music_list, 'warn': warn, 'user': user, 'today': today})
            
        if 'tg' in request.POST:
            cursor.execute(u""" Select * FROM [users] where [投稿次数] > 0 AND [用户名]=?""", user)
            tgcs = cursor.fetchall()

            if tgcs:
                tpa=int(0)
                mname = request.POST.get('mname')
                singer = request.POST.get('singer')
                if mname == '':
                    sql=u""" Select * FROM [musictg] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    music_list=[]
                    for row in list :
                        music=BorrowInfo(row[0],row[1],row[2])
                        music_list.append(music)
                    warn = u"歌曲名为空"
                    return render(request,'musictg.html',{'music_list':music_list, 'warn': warn, 'user': user, 'today': today})
                else:
                    cursor.execute(u""" Select * FROM [musictg] where [歌名]=?""", mname)
                    list=cursor.fetchall() 
                    if list:
                        warn= u"已有该歌曲，请勿重复投票！"
                    else:
                        sql = u"""INSERT INTO [musictg]([歌名],[歌手],[投票]) VALUES (?, ?, ?)"""
                        cursor.execute(sql, mname, singer, tpa)
                        cursor.execute(u""" update [users] set [投稿次数]=[投稿次数]-1 where [用户名]=? """, user)
                        warn= u"投稿成功！"
                        cz = "投稿"
                        yh = user
                        sj = datetime.now()
                        xx = request.META.get('REMOTE_ADDR')
                        czgq = mname
                        czxx = "投稿"
                        sql = u"""INSERT INTO [command]([操作],[用户],[时间],[信息],[操作歌曲],[操作信息]) VALUES (?, ?, ?, ?, ?, ?)"""
                        cursor.execute(sql,cz,yh,sj,xx,czgq,czxx)
                    sql=u""" Select * FROM [musictg] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    music_list=[]
                    for row in list :
                        music=BorrowInfo(row[0],row[1],row[2])
                        music_list.append(music)
                     

                return render(request,'musictg.html',{'music_list':music_list, 'user': user, 'today': today, 'warn': warn} )   
            else:
                warn= u"您没有剩余的投稿次数，请联系管理员获取或等待下周！"
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list : 
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)
                return render(request, 'musictg.html', {'music_list':music_list, 'warn': warn, 'user': user, 'today': today})

        else:
            global allow
            checkbox_list = request.POST.getlist("checkbox")
            cursor.execute(u""" Select * FROM [users] where [投票次数] > 0 and [用户名]=?""", user)
            tpcs = cursor.fetchall()
            nnum = 0
            if checkbox_list:
                if tpcs:
                    if allow != 1:
                        for li in checkbox_list:
                            cursor.execute(u""" update [musictg] set [投票]=[投票]+1 where [歌名]=? """, checkbox_list[nnum])
                            cz = "投票"
                            yh = user
                            sj = datetime.now()
                            xx = request.META.get('REMOTE_ADDR')
                            czgq = checkbox_list[nnum]
                            czxx = "投1票"
                            sql = u"""INSERT INTO [command]([操作],[用户],[时间],[信息],[操作歌曲],[操作信息]) VALUES (?, ?, ?, ?, ?, ?)"""
                            cursor.execute(sql,cz,yh,sj,xx,czgq,czxx)
                            nnum += 1
                        cursor.execute(u""" update [users] set [投票次数]=[投票次数]-1 where [用户名]=? """, user)
                        cursor.execute(u""" Select [投票次数] FROM [users] where [用户名]=?""", user)
                        tpcss = cursor.fetchone()
                        warn = u"您已经成功投票了" + str(nnum) + "首歌曲，剩余投票次数：" + str(tpcss[0]) + "次"
                        sql=u""" Select * FROM [musictg] order by [投票] desc"""
                        cursor.execute(sql)
                        list=cursor.fetchall()
                        music_list=[]
                        for row in list :                                       # 循环遍历
                            music=BorrowInfo(row[0],row[1],row[2])
                            music_list.append(music)                              # 将对象添加到传递到页面设计的列表
                        return render(request,'musictg.html',{'music_list':music_list, 'warn': warn, 'user': user, 'today': today} ) 
                    else:
                        warn= u"已锁榜，无法投票，请等待下周！"
                        sql=u""" Select * FROM [musictg] order by [投票] desc"""
                        cursor.execute(sql)
                        list=cursor.fetchall()
                        music_list=[]
                        for row in list : 
                            music=BorrowInfo(row[0],row[1],row[2])
                            music_list.append(music)
                        return render(request,'musictg.html',{'music_list':music_list, 'warn': warn, 'user': user, 'today': today} ) 
                else:
                    warn = u"您没有剩余的投票次数，请联系管理员获取或等待下周！"
            else:
                warn = u"未选择歌曲！"

        return render(request,'musictg.html',{'music_list':music_list, 'warn': warn, 'user': user, 'today': today} ) 

    else:
        return render(request,'musictg.html',{'music_list':music_list,'user': user, 'today': today} )
    
def pwdset(request): 
    if request.method =='POST':
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        pwd=str(request.POST.get('txtpwd'))
        pwd2=str(request.POST.get('txtpwd2'))
        user = request.session.get('user', '没有用户')
        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()
            if pwd == pwd2:
                cursor.execute(u""" update [users] set [密码]=? where [用户名]=? """, pwd , user)
                warn = u"修改成功！"
                request.session['user'] = user
                cz = "修改密码"
                yh = user
                sj = datetime.now()
                xx = request.META.get('REMOTE_ADDR')
                sql = u"""INSERT INTO [command]([操作],[用户],[时间],[信息]) VALUES (?, ?, ?, ?)"""
                cursor.execute(sql,cz,yh,sj,xx)
                return HttpResponseRedirect("/login")
            else:
                warn = u"两次输入的密码不一致，请重新输入！"
        except Exception as e:
            warn = u"ERROR：请联系服务器管理员！"
            print(e)
 
        cursor.close()
        conn.close()
        return render(request,'pwdset.html',{'warn':warn, 'user': user, 'today': today} )    
    else :      
        return render(request, 'pwdset.html')

def phblock(request):
    user = request.session.get('user', '没有用户')  # 获取session的值，没有时为'没有用户'
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 显示当前日期时间.如格式为：年-月-日 时：分：秒strftime('%Y-%m-%d %H:%M:%S')
    DBfile = os.getcwd() + u"""\数据库ftcd.mdb"""  # 起始执行目录\数据库文件
    conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
    cursor = conn.cursor()
    sql=u""" Select * FROM [phblock] order by [投票] desc"""
    cursor.execute(sql)
    list=cursor.fetchall()
    music_list=[]
    for row in list :                                       # 循环遍历
        music=BorrowInfo(row[0],row[1],row[2])
        music_list.append(music)
    return render(request,'phblock.html',{'music_list':music_list, 'user': user, 'today': today} ) 

 
def admlogin(request):
    if request.method == 'POST':
        admid = request.POST.get('txtuser')
        pwd = request.POST.get('txtpwd')
        warn = ''
        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()                            # 用游标方式
            cursor.execute(u""" Select * FROM [adminset] where [用户名]=?""", admid)
            list=cursor.fetchall()                            # 得到查询结果
  
            if list :                                         # 查询结果有内容
                for row in list :                             # 循环遍历                
                    if row[1]==pwd:                     # 查询于结果中密码等输入的密码
                        request.session['admid']=admid  # 设置session
                        return HttpResponseRedirect("/adminset")
                    else :
                        warn= u"用户不存在或密码错误！"
            else :
                warn = u"用户不存在或密码错误！"

        except Exception as e:
            warn= u"ERROR：请联系服务器管理员！"
            print(e)

        return render(request,'admlogin.html',{'warn':warn,'admid':admid})
    else:
        return render(request, 'admlogin.html') 
    
def admins(request):
    if request.method == 'POST':
        admaid = request.POST.get('txtuser')
        pwd = request.POST.get('txtpwd')
        warn = ''
        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()                            # 用游标方式
            cursor.execute(u""" Select * FROM [adminall] where [用户名]=?""", admaid)
            list=cursor.fetchall()                            # 得到查询结果
  
            if list :                                         # 查询结果有内容
                for row in list :                             # 循环遍历                
                    if row[1]==pwd:                     # 查询于结果中密码等输入的密码
                        request.session['admaid']=admaid  # 设置session
                        return HttpResponseRedirect("/adminall")
                    else :
                        warn= u"用户不存在或密码错误！"
            else :
                warn = u"用户不存在或密码错误！"

        except Exception as e:
            warn= u"ERROR：请联系服务器管理员！"
            print(e)

        return render(request,'admins.html',{'warn':warn,'admaid':admaid})
    else:
        return render(request, 'admins.html') 
    
def adminset(request):
    admid = request.session.get('admid', '没有用户')
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    DBfile = os.getcwd() + u"""\数据库ftcd.mdb"""
    conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)
    cursor = conn.cursor()
    sql=u""" Select * FROM [musictg] order by [投票] desc"""
    cursor.execute(sql)
    list=cursor.fetchall()
    music_list=[]
    for row in list :                                       # 循环遍历
        music=BorrowInfo(row[0],row[1],row[2])
        music_list.append(music)
    sql=u""" Select * FROM [adminset] where [用户名]=?"""   
    cursor.execute(sql, admid)
    data=cursor.fetchall()
    if data:
        pass
    else:
        return HttpResponseRedirect("http://ftcdstudio.com:520/ls/as.html")

    if request.method == 'POST':  # post方法
        global mname
        global singer
        global num
        sql=u""" Select * FROM [musictg] order by [投票] desc"""
        cursor.execute(sql)
        list=cursor.fetchall()
        music_list=[]
        for row in list :                                       # 循环遍历
            music=BorrowInfo(row[0],row[1],row[2])
            music_list.append(music)

        if 'ss' in request.POST:
            mname = request.POST.get('mname')
            if mname == '':
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)   
                warn = u"未输入信息"
                return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today})
            else:
                cursor.execute(u"""Select * FROM [musictg] where [歌名] =?""", mname)
                lists=cursor.fetchall()
                if lists:
                    music_list=[]
                    for row in lists :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        music_list.append(music)   
                    return render(request,'adminset.html',{'music_list':music_list, 'admid': admid, 'today': today} ) 
                else:
                    warn=u"未查询到结果！"
                    sql=u""" Select * FROM [musictg] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    music_list=[]
                    for row in list :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        music_list.append(music)   
                    return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
                
        if 'gs' in request.POST:
            sql1=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql1)
            list1=cursor.fetchall()
            if list1:
                warn= u"本周歌单已经审核完成，请勿重复操作"
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)
                return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
            else:
                sql = '''
                INSERT INTO yxlist
                select top 6 * from musictg order by [投票] desc
                '''
                cursor.execute(sql)
                warn= u"过审成功！"
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)
                return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
            
        if 'sc' in request.POST:
            checkbox_list = request.POST.getlist("checkbox")
            if checkbox_list:
                for item in checkbox_list:
                    sql = '''
                    DELETE FROM musictg
                    WHERE [歌名] = ?;
                    '''
                    cursor.execute(sql, (item,))
                warn= u"已删除！"
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)
                return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
            else:
                warn= u"未选择任何选项！"
                sql=u""" Select * FROM [musictg] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                music_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    music_list.append(music)
                return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
            
        if 'sb' in request.POST:
            global allow
            allow=1
            warn= u"已锁榜"
            sql=u""" Select * FROM [musictg] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            music_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                music_list.append(music)
            return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )
        
        if 'sx' in request.POST:
            warn= u"刷新列表成功！"
            sql=u""" Select * FROM [musictg] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            music_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                music_list.append(music)
            return render(request,'adminset.html',{'music_list':music_list, 'warn': warn, 'admid': admid, 'today': today} )

    else:
        return render(request,'adminset.html',{'music_list':music_list, 'admid': admid, 'today': today} )

def pwdset1(request): 
    if request.method =='POST':
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        pwd=str(request.POST.get('txtpwd'))
        pwd2=str(request.POST.get('txtpwd2'))
        admid = request.session.get('admid', '没有用户')
        try:
            DBfile = os.path.join(os.getcwd(), '数据库ftcd.mdb')  # 起始执行目录\数据库文件
            conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            cursor = conn.cursor()
            if pwd == pwd2:
                cursor.execute(u""" update [adminset] set [密码]=? where [用户名]=? """, pwd , admid)
                warn = u"修改成功！"
                request.session['admid'] = admid
                return HttpResponseRedirect("/admlogin")
            else:
                warn = u"两次输入的密码不一致，请重新输入！"
        except Exception as e:
            warn = u"ERROR：请联系服务器管理员！"
            print(e)
 
        cursor.close()
        conn.close()
        return render(request,'pwdset1.html',{'warn':warn, 'admid': admid, 'today': today} )    
    else :      
        return render(request, 'pwdset1.html')

def adminall(request):
    admaid = request.session.get('admaid', '没有用户')
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    DBfile = os.getcwd() + u"""\数据库ftcd.mdb"""
    conn = pyodbc.connect(u"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;", autocommit=True)
    cursor = conn.cursor()
    sql=u""" Select * FROM [adminall] where [用户名]=?"""   
    cursor.execute(sql, admaid)
    data=cursor.fetchall()
    sql=u""" Select * FROM [yxlist] order by [投票] desc"""
    cursor.execute(sql)
    list=cursor.fetchall()
    yx_list=[]
    warn=''
    for row in list :                                       # 循环遍历
        music=BorrowInfo(row[0],row[1],row[2])
        yx_list.append(music)
    sql=u""" Select * FROM [adminall] where [用户名]=?"""   
    cursor.execute(sql, admaid)
    data=cursor.fetchall()
    if data:
        pass
    else:
        return HttpResponseRedirect("http://ftcdstudio.com:520/ls/as.html")

    if request.method == 'POST':  # post方法
        sql=u""" Select * FROM [yxlist] order by [投票] desc"""
        cursor.execute(sql)
        list=cursor.fetchall()
        yx_list=[]
        for row in list :                                       # 循环遍历
            music=BorrowInfo(row[0],row[1],row[2])
            yx_list.append(music)

        if 'sousuom' in request.POST:
            mname = request.POST.get('mname')
            if mname == '':
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)   
                warn = u"未输入信息"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            else:
                cursor.execute(u"""Select * FROM [musictg] where [歌名] =?""", mname)
                lists=cursor.fetchall()
                if lists:
                    musicss_list=[]
                    for row in lists :                                       # 循环遍历
                        music=ssmInFo(row[0],row[1],row[2])
                        musicss_list.append(music) 
                    sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    yx_list=[]
                    for row in list :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        yx_list.append(music)  
                    return render(request,'adminall.html',{'yx_list':yx_list, 'musicss_list':musicss_list, 'admaid': admaid, 'today': today} ) 
                else:
                    warn=u"未查询到结果！"
                    sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    yx_list=[]
                    for row in list :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        yx_list.append(music)   
                    return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
                
        if 'sousuou' in request.POST:
            uph = request.POST.get('uph')
            if uph == '':
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)   
                warn = u"未输入信息"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            else:
                cursor.execute(u"""Select * FROM [users] where [手机号] =?""", uph)
                lists=cursor.fetchall()
                if lists:
                    userss_list=[]
                    for row in lists :                                       # 循环遍历
                        user=ssuInFo(row[0],row[1],row[2],row[3],row[4])
                        userss_list.append(user) 
                    sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    yx_list=[]
                    for row in list :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        yx_list.append(music)  
                    return render(request,'adminall.html',{'yx_list':yx_list, 'userss_list':userss_list, 'admaid': admaid, 'today': today} ) 
                else:
                    warn=u"未查询到结果！"
                    sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                    cursor.execute(sql)
                    list=cursor.fetchall()
                    yx_list=[]
                    for row in list :                                       # 循环遍历
                        music=BorrowInfo(row[0],row[1],row[2])
                        yx_list.append(music)   
                    return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'tongguo' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            sql1=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql1)
            list1=cursor.fetchall()
            if list1:
                sql = '''
                INSERT INTO phblock
                SELECT * FROM yxlist
                ORDER BY [投票] DESC;
                '''
                cursor.execute(sql)
                warn= u"已上榜！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)  
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            else:
                warn= u"允许列表内没有任何信息！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            
        if 'qingkong' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            sql1=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql1)
            list1=cursor.fetchall()
            if list1:
                sql = '''
                delete from yxlist
                '''
                cursor.execute(sql)
                warn= u"已清空允许列表！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)  
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            else:
                warn= u"允许列表内没有任何信息！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'chongzhi' in request.POST:
            global allow
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            sql = '''
            UPDATE users SET [投票次数] = 4
            '''
            cursor.execute(sql)
            sql = '''
            UPDATE users SET [投稿次数] = 1
            '''
            cursor.execute(sql)
            sql = '''
            delete from yxlist
            '''
            cursor.execute(sql)
            sql = '''
            DELETE FROM musictg
            WHERE [歌名] IN (SELECT TOP 6 [歌名] FROM musictg ORDER BY [投票] DESC)
            '''
            cursor.execute(sql)
            allow=0
            warn= u"已重置！"
            return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'chongzhirw' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            sql = '''
            delete from phblock
            '''
            cursor.execute(sql)
            warn= u"已重置！"
            return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'jiesuo' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            allow=0
            warn= u"已解除锁榜！"
            return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
                
        if 'd6' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            sql = '''
            DELETE FROM musictg
            WHERE [歌名] IN (SELECT TOP 6 [歌名] FROM musictg ORDER BY [投票] DESC)
            '''
            cursor.execute(sql)
            warn= u"已删除！"
            return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'gengpiao' in request.POST:
            try:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                piaoshu = int(request.POST.get('piaoshu'))
                checkbox_list = request.POST.getlist("checkbox")
                warn=''
                if checkbox_list:
                    for item in checkbox_list:
                        sql=u"""update musictg set [投票]=? where [歌名]=?"""
                        cursor.execute(sql,piaoshu,item)
                    warn = u"更改成功！"
                else:
                    warn = u"未选择歌曲！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            except:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                warn = u"ERROR:请输入正确信息！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'shanchu' in request.POST:
            checkbox_list = request.POST.getlist("checkbox")
            if checkbox_list:
                for item in checkbox_list:
                    sql = '''
                    DELETE FROM musictg
                    WHERE [歌名] = ?;
                    '''
                    cursor.execute(sql, (item,))
                warn= u"已删除！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            else:
                warn= u"未选择任何选项！"
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})

        if 'gengup' in request.POST:
            try:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                shuliang = request.POST.get('shuliang')
                checkbox_list = request.POST.getlist("checkbox")
                warn=''
                if checkbox_list:
                    for item in checkbox_list:
                        sql=u"""update users set [投票次数]=? where [用户名]=?"""
                        cursor.execute(sql,shuliang,item)
                    warn = u"更改成功！"
                else:
                    warn = u"未选择用户！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            except:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                warn = u"ERROR:请输入正确信息！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'gengug' in request.POST:
            try:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                shuliang = request.POST.get('shuliang')
                checkbox_list = request.POST.getlist("checkbox")
                warn=''
                if checkbox_list:
                    for item in checkbox_list:
                        sql=u"""update users set [投稿次数]=? where [用户名]=?"""
                        cursor.execute(sql,shuliang,item)
                    warn = u"更改成功！"
                else:
                    warn = u"未选择用户！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
            except:
                sql=u""" Select * FROM [yxlist] order by [投票] desc"""
                cursor.execute(sql)
                list=cursor.fetchall()
                yx_list=[]
                for row in list :                                       # 循环遍历
                    music=BorrowInfo(row[0],row[1],row[2])
                    yx_list.append(music)
                warn = u"ERROR:请输入正确信息！"
                return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
        
        if 'sx' in request.POST:
            sql=u""" Select * FROM [yxlist] order by [投票] desc"""
            cursor.execute(sql)
            list=cursor.fetchall()
            yx_list=[]
            for row in list :                                       # 循环遍历
                music=BorrowInfo(row[0],row[1],row[2])
                yx_list.append(music)
            return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})

    else:
        return render(request,'adminall.html',{'yx_list':yx_list, 'warn': warn, 'admaid': admaid, 'today': today})
