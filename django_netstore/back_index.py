from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from netstore.database import TbMember, TbBookinfo,Tbcart
from django.core import serializers
import json

def back_index(request):  #主界面后台逻辑
    ctx = {}
    html_str = 'back/index.html'
    if request.GET:
        if request.GET['keyword']=='quit':
            request.session['username']=''
        html_str = 'wap_login.html'
        return render(request, html_str, ctx)
    else:
        loginname=TbMember.objects.filter(username=str(request.session.get('username', '')))
        if request.session.get('username', ''):
            loginname = TbMember.objects.filter(username=str(request.session.get('username', '')[0]['username']))
        if loginname and loginname[0]['is_used']=='y':
                ctx['rlt'] = request.session.get('username', '')[0]['username']
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
            pagecount = TbMember.objects.count()
            if 'value' in request.GET:
                username = request.GET['value']
                if username:
                    db = TbMember.objects.filter(username=username)
                    pagecount=db.count()
                else:
                    db = TbMember.objects.all()
            elif 'editvalue' in request.GET:
                username=request.GET['username']
                password=request.GET['password']
                db = TbMember.objects(username=username).update(set__password=password)
            elif 'delvalue' in request.GET:
                db = TbMember.objects()
            else:
                db = TbMember.objects()
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



def shoplist(request):    #商品列表前段结构
    ctx = {}
    if request.GET:#加购物车，状态为：0，待审批为：1，审批完成为：2,
        if request.GET['keyword']=='addcart':
            itemid=request.GET['value']
            userid = request.session.get('username', '')[0]['userid']
            carthas=Tbcart.objects.filter(id=itemid,approval='0',userid=userid)
            itemname = TbBookinfo.objects.filter(id=itemid)
            if carthas:
                qty=carthas[0]['cartqty']
                Tbcart.objects.filter(itemid=itemid).update(cartqty=qty+1)
            elif Tbcart.objects.filter(approval='0',userid=userid):
                cartid=Tbcart.objects.filter(approval='0',userid=userid)
                addcart=Tbcart(cartid=cartid[0]['cartid'],itemid=itemid,cartname=itemname[0]['itemname'],cartqty='1',approval='0',price=itemname[0]['price_r'],memberid=itemname[0]['supplier'],userid=userid)
                addcart.save()
            else:
                addcart=Tbcart(cartid='111',itemid=itemid,cartname=itemname[0]['itemname'],cartqty='1',approval='0',price=str(itemname[0]['price_r']),memberid=itemname[0]['supplier'],userid=userid)
                addcart.save()
    ctx['keyword'] = 'shopinfo'
    db = TbBookinfo.objects.all()
    #ajax_testvalue = serializers.serialize("json", db)
    ctx['rlt'] =[x['itemname'] for x in db]
    ctx['bookde']=[y['supplier'] for y in db]
    ctx['id']=[str(x['id']) for x in db]
    return render(request, 'shoplist.html', ctx)

def shopadd(request):    #添加商品前端结构
    if request.POST:
        item_name=request.POST['itemname'].strip()
        item_id=request.POST['itemid'].strip()
        if item_name or item_id:
            item_name1=TbBookinfo.objects.filter(itemname=item_name)
            item_id1=TbBookinfo.objects.filter(itemid=item_id)
            if item_name1 or item_id1:
                ctx='数据库中已经有相应的商品名称或编号'
            else:
                obj = request.FILES.get('upload')
                price=request.POST['price'].strip()
                store=request.POST['qty'].strip()
                supplier=request.session.get('username', '')[0]['userid']
                detail=request.POST['detail'].strip()
                item=TbBookinfo(itemname=item_name,itemid=item_id,price_r=price,supplier=supplier,store=store,pic_path='upload/itempic/'+obj.name,detail=detail)
                item.save()
                item_name1 = TbBookinfo.objects.filter(itemname=item_name)
                if item_name1:
                    import os
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    f = open(os.path.join(BASE_DIR, 'upload', 'itempic', obj.name), 'wb')
                    for chunk in obj.chunks():
                        f.write(chunk)
                    f.close()
    return render(request, 'item_add.html')

