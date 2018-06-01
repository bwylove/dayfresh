# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect

from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
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
# 用户退出
def logout(request):
    request.session.flush()
    return redirect('/')
# 登陆用户中心
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
# 订单
@islogin
def order(request):
    context={'title':'用户中心','page_name':1,'order':1}
    return render(request,'df_user/user_center_order.html',context)
# 收获地址
@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uphone=post.get('uphone')
        user.ucode=post.get('ucode')
        user.save()
    context={'title':'用户中心','user':user,'page_name':1,'site':1}
    return render(request,'df_user/user_center_site.html',context)

# 此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
# 根据用户订单是否支付、下单顺序进行排序

def user_center_order(request,pageid):
    uid=request.session.get('user_id')
    orderinfos=OrderInfo.objects.filter(user_id=uid).order_by('zhifu','-oid')
    # 分页
    paginator=Paginator(orderinfos,2)

    orderlist=paginator.page(int(pageid))

    plist=paginator.page_range
    # 3页分页显示
    qian1=0
    hou=0
    hou2=0
    qian2=0
    dd=int(pageid)
    lenn=len(plist)

    if dd>1:
        qian1=dd-1
    if dd>3:
        qian2=dd-2
    if dd<lenn:
        hou=dd+1
    if dd+2<lenn:
        hou2=dd+2
    context={'page_name':1,'title':'全部订单','pageid':int(pageid),'order':1,'orderlist':orderlist,
             'plist':plist,'pre':qian1,'next':hou,'pree':qian2,'lenn':lenn,'nextt':hou2}
    return render(request,'df_user/user_center_order.html',context)