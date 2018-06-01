# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from df_cart.models import CartInfo
from df_user.islogin import islogin


@islogin
def cart(request):
    uid=request.session.get('user_id')
    carts=CartInfo.objects.filter(user_id=uid)
    lenn=len(carts)
    context={'title':'购物车','page_name':1,'carts':carts,'lenn':lenn}
    return render(request,'df_cart/cart.html',context)

@islogin
def delete(request,cart_id):
    cart=CartInfo.objects.get(pk=int(cart_id))
    cart.delete()
    count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
    request.session['count']=count
    data={'count':count}
    return JsonResponse(data)

@islogin
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data={'OK':0}
    except Exception as e:
        data={'OK':count1}
    return JsonResponse(data)


def add(request,gid,count):
    uid=request.session.get('user_id')
    gid=int(gid)
    count=int(count)
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)>=1:
        cart=carts[0]
        cart.count=cart.count+count
    else:
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
    cart.save()
    count_s=CartInfo.objects.filter(user_id=uid).count()
    request.session['count']=count_s
    if request.is_ajax():
        print '*'*10
        print 'ajax'
        return JsonResponse({'count':count_s})
    else:
        return redirect('/cart/')
