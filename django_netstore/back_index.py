from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from netstore.database import TbMember, TbBookinfo,Tbcart,Tbitempic,Tbcartid
from django.core import serializers
import json
import requests
import time
from datetime import datetime


def back_index(request):  #主界面后台逻辑
    ctx = {}
    html_str = 'back/index.html'
    if request.GET:
        if request.GET['keyword']=='quit':
            request.session['username']=''
        html_str = 'login.html'
        return render(request, html_str, ctx)
    else:
        loginname=TbMember.objects.filter(username=str(request.session.get('username', '')))
        if request.session.get('username', ''):
            loginname = TbMember.objects.filter(username=str(request.session.get('username', '')[0]['username']))
        if loginname and loginname[0]['is_used']=='y':
                ctx['rlt'] = request.session.get('username', '')[0]['realname']
                ctx['logo'] = loginname[0]['logo']
        else:
            ctx['rlt'] = '请先登录'
            html_str = '/wap/'
            return HttpResponseRedirect(html_str, ctx)
        return render(request, html_str, ctx)


def userinfotable(request):    #用户与商品信息生成json的函数
    request.encoding='utf-8'
    if 'keyword' in request.GET:
        page = request.GET['page']
        keyword = request.GET['keyword']
        limit = request.GET['limit']
        if keyword == 'userinfo':
            pagecount = TbMember.objects.filter(level='2').count()
            if 'value' in request.GET:
                username = request.GET['value']
                if username:
                    db = TbMember.objects.filter(username=username,level='2')
                    pagecount=db.count()
                else:
                    db = TbMember.objects.filter(level='2')
            elif 'editvalue' in request.GET:
                username=request.GET['username']
                password=request.GET['password']
                db = TbMember.objects(username=username).update(set__password=password)
            elif 'delvalue' in request.GET:
                username = request.GET['username']
                db = TbMember.objects.filter(username=username).delete()
            else:
                db = TbMember.objects.filter(level='2')
        elif keyword == 'memberinfo':
            pagecount = TbMember.objects.filter(level='1').count()
            if 'value' in request.GET:
                username = request.GET['value']
                if username:
                    db = TbMember.objects.filter(username=username,level='1')
                    pagecount=db.count()
                else:
                    db = TbMember.objects.filter(level='1')
            elif 'editvalue' in request.GET:
                username=request.GET['username']
                password=request.GET['password']
                db = TbMember.objects(username=username).update(set__password=password)
            elif 'delvalue' in request.GET:
                username = request.GET['username']
                db = TbMember.objects.filter(username=username).delete()
            else:
                db = TbMember.objects.filter(level='1')
        elif keyword=='shopinfo':
            supplier = request.session.get('username', '')[0]['userid']
            pagecount = TbBookinfo.objects.filter(supplier=supplier).count()
            if 'value' in request.GET:
                shopname = request.GET['value']
                if shopname:
                    db=TbBookinfo.objects.filter(itemname=shopname,supplier=supplier)
                    pagecount=db.count()
                else:
                    db = TbBookinfo.objects.filter(supplier=supplier)[(int(page) - 1) * int(limit):int(page)*int(limit)]
            else:
                db=TbBookinfo.objects.filter(supplier=supplier)[(int(page)-1)*int(limit):int(page)*int(limit)]
        elif keyword=='orderinfo':
            level=TbMember.objects.filter(username=str(request.session.get('username', '')[0]['username']))
            level1 = str(level[0]['level'])
            userid = level[0]['userid']
            if level1 == "1":
                db = Tbcart.objects.filter(memberid=userid, approval='2')
            else:
                db = Tbcart.objects.filter(userid=userid, approval='2')
                pagecount = db.count()
        elif 'editvalue' in request.GET:
            keyword = request.GET['keyword']
            if keyword == 'userinfo':
                username = request.GET['value']
    else:
        db = TbMember.objects()
        pagecount=0
    lendb=len(db)
    #ajax_testvalue = serializers.serialize("json", db)
    #m=json.loads(ajax_testvalue)
    data_db = []
    for m in range(0, lendb):
        fields = {}
        for n in db[m]:
            if n=='id':
                continue
            fields[n] = db[m][n]
        data_db.append(fields)
    data = {"code": 0, "msg": "", "count": pagecount, "data": data_db}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse(m[0]['fields'])
    #return JsonResponse(m[0]['fields'],safe=False)


def userinfo(request):  #用户信息端表结构
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'},{field:'realname', width:'8%', title: '用户名', sort: true} \
      ,{field:'password', width:'8%', title: '密码'} \
      ,{field:'email', width:'20%', title: '邮箱'} \
      ,{field:'phonecode', width:'15%', title: '电话'} \
      ,{field:'userid', width:'20%',title:'营业执照号码'} \
      ,{field:'register', width:'20%',title:'营业执照'} \
      ,{field:'is_used', width:'8%',title:'是否完善信息'} \
      ,{field:'username', width:'10%',title:'用户名'} \
      ,{field:'duty_people', width:'10%',title:'负责人'} \
      ,{field:'detail', width:'20%',title:'供应商详情'} \
      ,{fixed: 'right', width: 65, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='userinfo'

    return render(request,'back/userinfo.html',ctx)

def memberinfo(request):  #用户信息端表结构
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'},{field:'realname', width:'8%', title: '用户名', sort: true} \
      ,{field:'password', width:'8%', title: '密码'} \
      ,{field:'email', width:'20%', title: '邮箱'} \
      ,{field:'phonecode', width:'15%', title: '电话'} \
      ,{field:'userid', width:'20%',title:'营业执照号码'} \
      ,{field:'register', width:'20%',title:'营业执照'} \
      ,{field:'is_used', width:'8%',title:'是否完善信息'} \
      ,{field:'username', width:'10%',title:'用户名'} \
      ,{field:'duty_people', width:'10%',title:'负责人'} \
      ,{field:'detail', width:'20%',title:'供应商详情'} \
      ,{fixed: 'right', width: 65, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='memberinfo'

    return render(request,'back/userinfo.html',ctx)

def shopinfo(request):   #商品信息前段表结构
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'}\
      ,{field:'itemname', width:'30%', title: '商品名称', sort: true,edit:'text'} \
      ,{field:'itemid', width:'20%', title: '商品编号'} \
      ,{field:'price_r', width:'10%', title: '价格',edit:'text'} \
      ,{field:'store', width:'15%', title: '库存',edit:'text'} \
      ,{field:'price_n', width:'8%',title:'上架日期',edit:'text'} \
      ,{field:'pic_path', width:'10%',title:'图片',templet: '#imgTpl',edit:'text'} \
      ,{field:'supplier', width:'10%',title:'上传人',edit:'text'} \
      ,{field:'detail', width:'10%',title:'商品详情',edit:'text'} \
      ,{fixed: 'right', width: 65, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='shopinfo'


    return render(request,'back/userinfo.html',ctx)

def orderinfo(request):
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'}\
      ,{field:'cartid', width:'30%', title: '订单号', sort: true,edit:'text'} \
      ,{field:'username', width:'20%', title: '采购方'} \
      ,{field:'membername', width:'10%', title: '供应商',edit:'text'} \
      ,{field:'ordertime', width:'15%', title: '生成时间',edit:'text'} \
      ,{fixed: 'right', width: 65, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='orderinfo'
    return render(request,'back/userinfo.html',ctx)

def shoplist(request):    #商品列表前段结构
    ctx = {}
    if request.GET:#加购物车，状态为：0，待审批为：1，审批完成为：2,
        if request.GET['keyword']=='addcart':
            itemid=request.GET['value']
            userid = request.session.get('username', '')[0]['userid']
            username=request.session.get('username', '')[0]['realname']
            carthas=Tbcart.objects.filter(itemid=itemid,approval='0',userid=userid)
            itemname = TbBookinfo.objects.filter(id=itemid)
            membername=TbMember.objects.filter(userid=itemname[0]['supplier'])
            if carthas:
                qty=carthas[0]['cartqty']
                cartqty=str(int(qty)+1)
                Tbcart.objects.filter(itemid=itemid).update(cartqty=cartqty)
            elif Tbcart.objects.filter(approval='0',userid=userid):
                cartid=Tbcart.objects.filter(approval='0',userid=userid)
                addcart1=Tbcart(cartid=cartid[0]['cartid'],itemid=itemid,cartname=itemname[0]['itemname'],cartqty='1',approval='0',price=str(itemname[0]['price_r']),memberid=membername[0]['realname'],membername=membername[0]['realname'],userid=userid,username=username)
                addcart1.save()
            else:
                addcartid=Tbcartid(cartmemberid=userid)
                addcartid.save()
                cartid=Tbcartid.objects.filter(cartmemberid=userid)
                addcart2=Tbcart(cartid=str(cartid[0]['id']),itemid=itemid,cartname=itemname[0]['itemname'],cartqty='1',approval='0',price=str(itemname[0]['price_r']),memberid=itemname[0]['supplier'],membername=membername[0]['realname'],userid=userid,username=username)
                addcart2.save()
                Tbcartid.objects.filter(cartmemberid=userid).delete()
    ctx['keyword'] = 'shopinfo'
    db = TbBookinfo.objects.all()
    ctx['html1']=''
    m=0
    for x in db:
    #ajax_testvalue = serializers.serialize("json", db)
        m+=1
        bookpic = x['pic_path']
        rlt = x['itemname']
        supplier = x['supplier']
        ctx['html1']=ctx['html1']+'<div class="layui-col-sm4 layui-col-md3 layui-col-lg2">\
      <div class="layui-card"><div class="list_num red">'+str(m)+'</div>\
    <div class="pic" align="center"><a href="" target="_blank"><img src="'+x['pic_path']+'" width="150" height="150" alt="2345" title="2345"></a></div>\
    <div class="name"><b href="" target="_blank" title="2345">'+x['itemname']+'</b></div>\
    <div class="star"><span class="level"><span style="width: 95.6%;"></span></span></div>\
    <div class="publisher_info">供货商:&nbsp;<a href="">'+x['supplier']+'</a></div>\
    <div class="publisher_info"><span>  库存：</span>&nbsp;<a href="" target="_blank">&nbsp'+str(x['store'])+'件</a></div> <div class="price">\
    <p><span class="price_n">￥'+str(x['price_r'])+'</span><span class="price_r">￥'+str(x['price_r'])+'</span></p>\
    <div class="buy_button"><a ddname="加入购物车" onclick="addcart('+str(m)+')" class="listbtn_buy">加入购物车</a><a name="" href="" class="listbtn_buydz" target="_blank">商品详情</a></div>\
    </div></div></div>'
    ctx['rlt'] =[x['itemname'] for x in db]
    ctx['bookde']=[y['supplier'] for y in db]
    ctx['id']=[str(x['id']) for x in db]
    ctx['bookpic']=[str(x['pic_path']) for x in db]
    ctx['price'] = [str(x['price_r']) for x in db]
    return render(request, 'shoplist.html', ctx)

def shopadd(request):    #添加商品前端结构
    if request.POST:
        item_name=request.POST['itemname'].strip()
        item_id=request.POST['itemid'].strip()
        userid = request.session.get('username', '')[0]['userid']
        if item_name or item_id:
            item_name1=TbBookinfo.objects.filter(itemname=item_name,supplier=userid)
            item_id1=TbBookinfo.objects.filter(itemid=item_id,supplier=userid)
            if item_name1 or item_id1:
                ctx='数据库中已经有相应的商品名称或编号'
            else:
                obj_main = request.FILES.get('upload')
                obj_banner1=request.FILES.get('upload1-1')
                obj_banner2 = request.FILES.get('upload1-2')
                obj_banner3 = request.FILES.get('upload1-3')
                obj_banner4 = request.FILES.get('upload1-4')
                obj_detail1 = request.FILES.get('upload2-1')
                obj_detail2 = request.FILES.get('upload2-2')
                obj_detail3 = request.FILES.get('upload2-3')
                obj_detail4 = request.FILES.get('upload2-4')
                obj_detail5 = request.FILES.get('upload2-5')
                import os
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                price=request.POST['price'].strip()
                store=request.POST['qty'].strip()
                supplier=request.session.get('username', '')[0]['userid']
                item=TbBookinfo(itemname=item_name,itemid=item_id,price_r=price,supplier=supplier,store=store,pic_path='/upload/itempic/'+item_name+obj_main.name)
                item.save()
                item_name1 = TbBookinfo.objects.filter(itemname=item_name,supplier=userid)
                itemid=str(item_name1[0]['id'])
                if obj_banner1:

                    item_pic1_1 = Tbitempic(picid='1', picclass='1', picpath='/upload/itempic/'+itemid+'_banner'+obj_banner1.name, itemid=itemid)
                    item_pic1_1.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_banner' + obj_banner1.name), 'wb')
                    for chunk in obj_banner1.chunks():
                        f.write(chunk)
                    f.close()
                if obj_banner2:
                    item_pic1_2 = Tbitempic(picid='2', picclass='1', picpath='/upload/itempic/' + itemid+'_banner'+obj_banner2.name,
                                            itemid=itemid)
                    item_pic1_2.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_banner' + obj_banner2.name), 'wb')
                    for chunk in obj_banner2.chunks():
                        f.write(chunk)
                    f.close()
                if obj_banner3:
                    item_pic1_3 = Tbitempic(picid='3', picclass='1', picpath='/upload/itempic/' + itemid+'_banner'+obj_banner3.name,
                                            itemid=itemid)
                    item_pic1_3.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_banner' + obj_banner3.name), 'wb')
                    for chunk in obj_banner3.chunks():
                        f.write(chunk)
                    f.close()
                if obj_banner4:
                    item_pic1_4 = Tbitempic(picid='4', picclass='1', picpath='/upload/itempic/' + itemid+'_banner'+obj_banner4.name,
                                        itemid=itemid)
                    item_pic1_4.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_banner' + obj_banner4.name), 'wb')
                    for chunk in obj_banner4.chunks():
                        f.write(chunk)
                    f.close()
                if obj_detail1:
                    item_pic2_1 = Tbitempic(picid='1', picclass='2', picpath='/upload/itempic/' + itemid+'_detail'+obj_detail1.name,
                                        itemid=itemid)
                    item_pic2_1.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_detail' + obj_detail1.name), 'wb')
                    for chunk in obj_detail1.chunks():
                        f.write(chunk)
                    f.close()
                if obj_detail2:
                    item_pic2_2 = Tbitempic(picid='2', picclass='2', picpath='/upload/itempic/' + itemid+'_detail'+obj_detail2.name,
                                            itemid=itemid)
                    item_pic2_2.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_detail' + obj_detail2.name), 'wb')
                    for chunk in obj_detail2.chunks():
                        f.write(chunk)
                    f.close()
                if obj_detail3:
                    item_pic2_3 = Tbitempic(picid='3', picclass='2', picpath='/upload/itempic/' + itemid+'_detail'+obj_detail3.name,
                                        itemid=itemid)
                    item_pic2_3.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_detail' + obj_detail3.name), 'wb')
                    for chunk in obj_detail3.chunks():
                        f.write(chunk)
                    f.close()
                if obj_detail4:
                    item_pic2_4 = Tbitempic(picid='4', picclass='2', picpath='/upload/itempic/' + itemid+'_detail'+obj_detail4.name,
                                        itemid=itemid)
                    item_pic2_4.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_detail' + obj_detail4.name), 'wb')
                    for chunk in obj_detail4.chunks():
                        f.write(chunk)
                    f.close()
                if obj_detail5:
                    item_pic2_5 = Tbitempic(picid='5', picclass='2', picpath='/upload/itempic/' + itemid+'_detail'+obj_detail5.name,
                                        itemid=itemid)
                    item_pic2_5.save()
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', itemid + '_detail' + obj_detail5.name), 'wb')
                    for chunk in obj_detail5.chunks():
                        f.write(chunk)
                    f.close()
                if item_name1:
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', item_name+obj_main.name), 'wb')
                    for chunk in obj_main.chunks():
                        f.write(chunk)
                    f.close()
    return render(request, 'item_add.html')


#def cart_approval(request):
def cart(request): #购物车界面后台代码
    if request.POST:
        req =request.POST.getlist('cart[]')
       # req="'cart[]': ['{id:5ca32fde2689141b5c26e1d3,qty:1}', '{id:5ca36d3926891434bc584013,qty:1}'], 'csrfmiddlewaretoken': ['69rxp8xDFQD5GyOxH0U9io14SCBFQZISOD6aA0xJu4f4qTGNMuSGqpXhv3ioXkKV'']}"
        for n in req:
            m=eval(n)
            Tbcart.objects.filter(id=str(m['id'])).update(cartqty=str(m['qty']),approval='1')
        return render(request,'cart.html')
    elif request.GET:
        if request.GET['keyword']=='delete':
            itemid=request.GET['id']
            Tbcart.objects.filter(id=itemid).delete()
            return render(request,'cart.html')
    else:
        poststr={}
        ctx={}
        ctx['com']=''
        ctx['rlt']=''
        userid = request.session.get('username', '')[0]['userid']
        itemcart=Tbcart.objects.filter(userid=userid,approval='0')
        membernamelast=''
        price_sum = 0
        m=0
        for n in itemcart:
            m+=1
            membernamenow = n['memberid']
            price=n['price']
            item=TbBookinfo.objects.filter(id=n['itemid'])
            itempic=item[0]['pic_path']
            frontqty=n['cartqty']
            cartname=n['cartname']
            price_sum = price_sum + float(price) * float(frontqty)
            ctx['foot'] = '</div>\
                        </div>\
                        <br>'
            if membernamelast == membernamenow:
                membernamenow = membernamelast
                ctx['foot'] = '</div>\
                            <br>'
            else:
                if TbMember.objects.filter(userid=membernamenow):
                    member = TbMember.objects.filter(userid=membernamenow)
                    if member[0]['realname']:
                        membername=member[0]['realname']
                    else:
                        membername='该账号已注销'
                else:
                    membername = membernamenow
                ctx['com']=ctx['com']+'<div>\
        <div class="layui-col-md2" align="center">\
        <b>'+membername+'</b>\
        </div>\
        <hr class="layui-bg-green">'
            membernamelast=membernamenow
            ctx['rlt']='<blockquote class="layui-elem-quote" id="'+str(n['id'])+'">\
                <div class="layui-row layui-col-space10">\
              <div class="layui-col-md2" align="center">\
                <img src="'+itempic+'" height="80" width="80" style="border:1px solid black"/>\
              </div>\
              <div class="layui-col-md4" style="vertical-align:middle">\
                <a>'+cartname+'</a><div class="wy-pro-pri fl">单价：<em class="num font-15" id="price'+str(m)+'">'+price+'</em></div>\
              </div>\
              <div class="layui-col-md4" align="center">\
                  <a>数量:       </a><button class="layui-btn layui-btn-primary layui-btn-sm" onclick="add('+str(m)+')">+</button><input id="'+str(m)+'" type="text" size="2" value="'+frontqty+'" align="center"><button  class="layui-btn layui-btn-primary layui-btn-sm" onclick="del('+str(m)+')">-</button>\
              </div><div class="layui-col-md2" align="center"><div class="wy-pro-pri fl">合计：<em class="num font-15" id="price'+str(m)+'">'+str(float(price)*int(frontqty))+'</em></div></div> <div class="layui-col-md2" align="center"><button class="layui-btn layui-btn-danger" onclick="del_item('+str(m)+')">删除商品</button></div>\
            </div></blockquote><hr>'
            ctx['com'] = ctx['com'] + ctx['rlt']

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

        return render(request,'cart.html',ctx)

def order(request):
    if request.session['username']:
        level=TbMember.objects.filter(username=str(request.session.get('username', '')))
        level1=level[0]['level']
        userid=level[0]['userid']
        if level1==0:
            order=Tbcart.objects.filter(memberid=userid,approval='2')
        else:
            order=Tbcart.objects.filter(userid=userid,approval='2')


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
        memberidlast=''
        m=0
        price_sum=0
        price_sum_order=0
        for n in itemcart:
            m+=1
            memberidnow = n['cartid']
            membernameid = n['memberid']
            price = n['price']
            qty = n['cartqty']
            price_sum = price_sum + float(price) * float(qty)
            price_sum_order+= float(price) * float(qty)
            item=TbBookinfo.objects.filter(id=n['itemid'])
            itempic=item[0]['pic_path']
            frontqty=n['cartqty']
            cartname=n['cartname']
            ctx['foot'] = ''
            if TbMember.objects.filter(userid=membernameid):
                member = TbMember.objects.filter(userid=membernameid)
                if member[0]['realname']:
                    membername = member[0]['realname']
                else:
                    membername = '该账号已注销'
            else:
                membername = '该账号不存在'
            if memberidlast == memberidnow:
                memberidnow = memberidlast
                ctx['foot'] = '</div>'
            else:
                price_sum_order -= float(price) * float(qty)
                ctx['foot'] = '<div align="right">合计价格：'+str(price_sum_order)+'</div></div>'
                price_sum_order=float(price) * float(qty)
                if ctx['com']=='':
                    ctx['foot']='</div>'
                ctx['com']=ctx['com']+ctx['foot']+'<div class="weui-panel weui-panel_access">\
                <div class="layui-row layui-col-space10"><div class="layui-col-md4"><b id="+memberidnow+">订单号：' + memberidnow + '</b></div><div class="layui-form layui-col-md2"><div class="layui-form-item"><div class="layui-input-block"><input type="checkbox" name="like[write]" title="确定审核"><div class="layui-unselect layui-form-checkbox"><span>确定审核</span><i class="layui-icon layui-icon-ok"></i></div></div></div></div><hr class="layui-bg-green"></div></div>'
            memberidlast = memberidnow
            ctx['rlt'] = '<blockquote class="layui-elem-quote" id="' + str(n['id']) + '">\
                            <div class="layui-row layui-col-space10">\
                          <div class="layui-col-md2" align="center">\
                            <img src="' + itempic + '" height="80" width="80" style="border:1px solid black"/>\
                          </div>\
                          <div class="layui-col-md4" style="vertical-align:middle">\
                            <a>' + cartname + '</a>\
                          </div>\
                              <div class="layui-col-md4" align="center"><a>商家:</a><a>' + membername + '</a></div>\
                            <div class="layui-col-md2" align="center"><a>数量:</a><a>' + frontqty + '</a>\
                        </div></blockquote><hr>'
            ctx['com'] = ctx['com'] + ctx['rlt']
            if m==len(itemcart):
                ctx['foot'] = '<div align="right">合计价格：'+str(price_sum_order)+'</div></div>'
            else:
                ctx['foot'] = '</div>'
            ctx['com'] = ctx['com'] + ctx['foot']
            ctx['rlt'] = ''
            ctx['foot'] = ''
        ctx['price'] = str(price_sum)
        '''
        if request.POST['name']=='delete':
            poststr['id']=request.POST['id']
            Tbcart.objects.filter(cartid=poststr['id']).delete()
        elif request.POST['name']=='submit':
            poststr['id']=request.POST['id']
            poststr['qty']=request.POST['qty']
    '''

        return render(request,'confirm.html',ctx)


