# -*- coding: utf-8 -*-
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect

from df_goods.models import GoodsInfo
from models import *
from hashlib import sha1
from .islogin import islogin



def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接受用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    # 判断两次密码输入是否一致
    if upwd!=upwd2:
        return redirect('/user/register/')
    # 加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    # 创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    # 注册成功，转到登陆页面
    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 接受请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    # 根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)
    print uname
    # 判断：如果未查到则用户名错，如果查到则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            red=HttpResponseRedirect('/user/info')
            # 记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uanem','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)

@islogin
def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    # 最近浏览记录
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_id_list=goods_ids.split(',')
    goods_list=[]
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context={'title':'用户中心',
             'user_email':user_email,
             'user_name':request.session['user_name'],
             'page':1,
             'info':1,
             'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)