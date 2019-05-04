from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from netstore.database import TbMember, TbBookinfo,Tbcart,Tbitempic
from django.core import serializers
import requests
import time
from datetime import datetime
import os
import json

def test(request):
    r=requests.get('http://www.byscience.net')
    date1=r.headers["Date"]
    ctx={}
    ltime= time.strptime(date1[5:25], "%d %b %Y %H:%M:%S")
     #把字符串,转换为为时间格式
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    atime=time.strftime('%Y-%m-%d %H:%M:%S',ttime)
    #mtime=time.mktime(ltime)+28800 #把时间变更为时间戳，+8*60*60 8个小时为北京时间 ,相加
    #ttime=time.localtime(mtime)#把时间戳转换为本地时间格式
    #d="%d-%d-%d"%(date.tm_year,date.tm_mon,date.tm_mday)
    #t="%d:%d:%d"%(date.tm_hour,date.tm_min,date.tm_sec)
    time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    a=datetime.now().strftime("%H:%M:%S")
    ctx['test']=atime
    return render(request, 'test.html',ctx)

def shopcart(request): #购物车界面后台代码
    if request.POST:
        req =request.POST.getlist('cart[]')
       # req="'cart[]': ['{id:5ca32fde2689141b5c26e1d3,qty:1}', '{id:5ca36d3926891434bc584013,qty:1}'], 'csrfmiddlewaretoken': ['69rxp8xDFQD5GyOxH0U9io14SCBFQZISOD6aA0xJu4f4qTGNMuSGqpXhv3ioXkKV'']}"
        for n in req:
            m=eval(n)
            Tbcart.objects.filter(id=str(m['id'])).update(cartqty=str(m['qty']),price=str(m['price']),approval='1',)
        return render(request,'app/shopcart.htm')
    elif request.GET:
        if request.GET['keyword']=='delete':
            itemid=request.GET['id']
            Tbcart.objects.filter(id=itemid).delete()
            return render(request,'app/shopcart.htm')
    else:
        poststr={}
        ctx={}
        ctx['com']=''
        ctx['rlt']=''
        userid = request.session.get('username', '')[0]['userid']
        itemcart=Tbcart.objects.filter(userid=userid,approval='0')
        membernamelast=''
        m=0
        price_sum=0
        for n in itemcart:
            m+=1
            membernamenow = n['memberid']
            price = n['price']
            qty=n['cartqty']
            price_sum=price_sum+float(price)*float(qty)
            item=TbBookinfo.objects.filter(id=n['itemid'])
            itempic=item[0]['pic_path']
            frontqty=n['cartqty']
            cartname=n['cartname']
            if membernamelast == membernamenow:
                membernamenow = membernamelast
            else:
                if TbMember.objects.filter(userid=membernamenow):
                    member = TbMember.objects.filter(userid=membernamenow)
                    if member[0]['realname']:
                        membername=member[0]['realname']
                    else:
                        membername='该账号已注销'
                else:
                    membername = membernamenow
                ctx['com']=ctx['com']+'<div class="weui-panel weui-panel_access">\
                <div class="weui-panel__hd"><span>' + membername + '</span><a href="javascript:;" class="wy-dele" ></a></div>'
            ctx['rlt']= '<div class="weui-panel__bd" id="' + str(n['id']) + '"> <div class="weui-media-box_appmsg pd-10"><div class="weui-media-box__hd check-w weui-cells_checkbox"></div>\
                    <div class="weui-media-box__hd"><a href=""><img class="weui-media-box__thumb" src="' + itempic + '" alt=""></a></div>\
                    <div class="weui-media-box__bd"> <h1 class="weui-media-box__desc"><b href="">' + cartname + '</b></h1>\
                      <p class="weui-media-box__desc">规格：<span>红色</span>，<span>23</span></p>\
                      <div class="clear mg-t-10">  <div class="wy-pro-pri fl">¥<em class="num font-15" id="price'+str(m)+'">'+price+'</em></div><div class="pro-amount fr"><div class="Spinner"><a class="DisDe" align="center" href="javascript:void(0)" onclick="del(' + str(
                m) + ')">-</a><input id="' + str(
                m) + '" class="Amount" value="' + frontqty + '" autocomplete="off" maxlength="3"><a class="Increase" href="javascript:void(0)" onclick="add(' + str(
                m) + ')">+</a></div></div>\
                      </div></div></div></div></div>'
            ctx['com'] = ctx['com'] + ctx['rlt']
            ctx['foot']='</div>\
            </div>\
            <br>'
            ctx['com']=ctx['com']+ctx['foot']
            ctx['rlt']=''
            ctx['foot']=''
        ctx['price'] = str(price_sum)
        '''
        if request.POST['name']=='delete':
            poststr['id']=request.POST['id']
            Tbcart.objects.filter(cartid=poststr['id']).delete()
        elif request.POST['name']=='submit':
            poststr['id']=request.POST['id']
            poststr['qty']=request.POST['qty']
    '''

        return render(request,'app/shopcart.htm',ctx)

def confirm(request): #购物车界面后台代码
    if request.POST:
        req =request.POST.getlist('cart[]')
       # req="'cart[]': ['{id:5ca32fde2689141b5c26e1d3,qty:1}', '{id:5ca36d3926891434bc584013,qty:1}'], 'csrfmiddlewaretoken': ['69rxp8xDFQD5GyOxH0U9io14SCBFQZISOD6aA0xJu4f4qTGNMuSGqpXhv3ioXkKV'']}"
        for n in req:
            m=eval(n)
            r = requests.get('http://www.byscience.net')
            date1 = r.headers["Date"]
            ctx = {}
            ltime = time.strptime(date1[5:25], "%d %b %Y %H:%M:%S")
            # 把字符串,转换为为时间格式
            ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
            atime = time.strftime('%Y-%m-%d %H:%M:%S', ttime)
            Tbcart.objects.filter(id=str(m['id'])).update(price=str(m['price']),approval='2',ordertime=str(atime))
        return render(request,'app/confirm.htm')
    elif request.GET:
        if request.GET['keyword']=='delete':
            itemid=request.GET['id']
            Tbcart.objects.filter(id=itemid).delete()
            return render(request,'app/confirm.htm')
    else:
        poststr={}
        ctx={}
        ctx['com']=''
        ctx['rlt']=''
        ctx['test']=''
        userid = request.session.get('username', '')[0]['userid']
        itemcart=Tbcart.objects.filter(userid=userid,approval='1')
        membernamelast=''
        m=0
        price_sum=0
        for n in itemcart:
            m+=1
            membernamenow = n['memberid']
            price = n['price']
            qty = n['cartqty']
            price_sum = price_sum + float(price) * float(qty)
            item=TbBookinfo.objects.filter(id=n['itemid'])
            itempic=item[0]['pic_path']
            frontqty=n['cartqty']
            cartname=n['cartname']
            ctx['foot'] = ''
            if membernamelast == membernamenow:
                membernamenow = membernamelast
            else:
                if TbMember.objects.filter(userid=membernamenow):
                    member = TbMember.objects.filter(userid=membernamenow)
                    if member[0]['realname']:
                        membername=member[0]['realname']
                    else:
                        membername='该账号已注销'
                else:
                    membername = membernamenow
                ctx['foot'] = '</div>'
                ctx['com'] = ctx['com'] + ctx['foot']
                ctx['com']=ctx['com']+'<div class="weui-panel weui-panel_access">\
                <div class="weui-panel__hd"><span>' + membername + '</span><a href="javascript:;" class="wy-dele" ></a></div>'


            ctx['rlt']= '<div class="weui-panel__bd" id="' + str(n['id']) + '"> <div class="weui-media-box_appmsg pd-10"><div class="weui-media-box__hd check-w weui-cells_checkbox"></div>\
                    <div class="weui-media-box__hd"><a href=""><img class="weui-media-box__thumb" src="' + itempic + '" alt=""></a></div>\
                    <div class="weui-media-box__bd"> <h1 class="weui-media-box__desc"><b href="">' + cartname + '</b></h1>\
                      <p class="weui-media-box__desc">规格：<span>红色</span>，<span>23</span></p>\
                      <div class="clear mg-t-10">  <div class="wy-pro-pri fl">¥<em class="num font-15" id="price'+str(m)+'">'+price+'</em></div><div class="pro-amount fr"><div class="Spinner"><a class="DisDe" align="center" href="javascript:void(0)" onclick="del(' + str(
                m) + ')">-</a><input id="' + str(
                m) + '" class="Amount" value="' + frontqty + '" autocomplete="off" maxlength="3"><a class="Increase" href="javascript:void(0)" onclick="add(' + str(
                m) + ')">+</a></div></div>\
                      </div></div></div></div>'
            ctx['com'] = ctx['com'] + ctx['rlt']


            ctx['rlt']=''
            membernamelast = membernamenow
        ctx['foot'] = '</div>'
        ctx['com'] = ctx['com'] + ctx['foot']
        ctx['price'] = str(price_sum)
        '''
        if request.POST['name']=='delete':
            poststr['id']=request.POST['id']
            Tbcart.objects.filter(cartid=poststr['id']).delete()
        elif request.POST['name']=='submit':
            poststr['id']=request.POST['id']
            poststr['qty']=request.POST['qty']
    '''

        return render(request,'app/confirm.htm',ctx)

def shopdetail(request):
    ctx={}

    if request.GET:
        itemid=request.GET['id']
    else:
        itemid='5cc3e2bf268914469c00b149'
    item=TbBookinfo.objects.filter(id=itemid)
    memberinfo=TbMember.objects.filter(userid=item[0]['supplier'])
    pic1=Tbitempic.objects.filter(itemid=itemid,picclass='1')
    pic2=Tbitempic.objects.filter(itemid=itemid,picclass='2')
    ctx['itemname']=item[0]['itemname']
    ctx['price']=item[0]['price_r']
    ctx['member']=item[0]['supplier']
    ctx['logo']=memberinfo[0]['logo']
    ctx['store']=item[0]['store']
    ctx['pic1']=''
    ctx['pic2']=''
    ctx['id']=itemid
    userid = request.session.get('username', '')[0]['userid']
    itemcart = Tbcart.objects.filter(userid=userid, approval='0')
    ctx['cartcount']=0
    for n in itemcart:
        ctx['cartcount']+=int(n['cartqty'])
    for x in pic2:
        ctx['pic2']+='<img src="'+x['picpath']+'" width="100%">'
    for x in pic1:
        ctx['pic1']+='<div class=""><img src="'+x['picpath']+'" width="300"></div>'
    return render(request, 'app/shopdetail.html', ctx)