# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from df_goods.models import GoodsInfo,TypeInfo


def index(request):

    count=request.session.get('count')

    fruit=GoodsInfo.objects.filter(gtype__id=2).order_by("-id")[:4]

    fruit2 = GoodsInfo.objects.filter(gtype__id=2).order_by("-gclick")[:4]

    seafood=GoodsInfo.objects.filter(gtype__id=4).order_by("-id")[:4]

    seafood2 = GoodsInfo.objects.filter(gtype__id=4).order_by("-gclick")[:4]

    meat=GoodsInfo.objects.filter(gtype__id=1).order_by("-id")[:4]

    meat2 = GoodsInfo.objects.filter(gtype__id=1).order_by("-gclick")[:4]

    egg = GoodsInfo.objects.filter(gtype__id=5).order_by("-id")[:4]

    egg2 = GoodsInfo.objects.filter(gtype__id=5).order_by("-gclick")[:4]

    vegetables = GoodsInfo.objects.filter(gtype__id=3).order_by("-id")[:4]

    vegetables2 = GoodsInfo.objects.filter(gtype__id=3).order_by("-gclick")[:4]

    ice = GoodsInfo.objects.filter(gtype__id=6).order_by("-id")[:4]

    ice2 = GoodsInfo.objects.filter(gtype__id=6).order_by("-gclick")[:4]

    context={'title':'首页','fruit':fruit,'seafood':seafood,'meat':meat,'egg':egg,'vegetables':vegetables,'ice':ice,
             'fruit2': fruit2, 'seafood2': seafood2, 'meat2': meat2, 'egg2': egg2, 'vegetables2': vegetables2, 'ice2': ice2,'guest_cart':1,'page_name':0,'count':count}

    return render(request,'df_goods/index.html',context)

def goodlist(request,typeid,pageid,sort):

    count=request.session.get('count')

    newgood=GoodsInfo.objects.all().order_by('-id')[:2]

    if sort=='1':

        sumGoodList=GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')

    elif sort=='2':

        sumGoodList=GoodsInfo.objects.filter(gtype_id=typeid).order_by('gprice')

    elif sort=='3':

        sumGoodList=GoodsInfo.objects.filter(gtype_id=typeid).order_by('-gclick')

    paginator=Paginator(sumGoodList,15)

    goodList=paginator.page_range(int(pageid))

    pindexList=paginator.page_range

    goodtype=TypeInfo.objects.get(id=typeid)

    context={'title':'商品详情','list':1,'guest_cart':1,'goodtype':goodtype,'newgood':newgood,'goodList':goodList,
             'typeid':typeid,'sort':sort,'pindexList':pindexList,'pageid':int(pageid),'count':count}

    return render(request,'df_goods/list.html',context)

def detail(request,typeid,pageid,sort):

    goods=GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()

    goodtype=goods.gtype

    count=request.session.get('count')

    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    context={'title':goods.gtype.ttitle,'guest_cart':1,'g':goods,'newgood':news,'id':id,'isDetail':True,'list':1,'goodtype':goodtype,'count':count}

    response=render(request,'df_goods/detail.html',context)

    goods_ids=request.COOKIES.get('goods_ids','')

    goods_id='%d'%goods.id

    if goods_ids!='':

        goods_id_list=goods_ids.split(',')

        if goods_id_list.count(goods_id)>=1:

            goods_id_list.remove(goods_id)

        goods_id_list.insert(0,goods_id)

        if len(goods_id_list)>=6:

            del goods_id_list[5]

        goods_ids=','.join(goods_id_list)

    else:

        goods_ids=goods_id

    response.set_cookie('goods_ids',goods_ids)

    return response