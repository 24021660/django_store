from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from netstore.sqldatabase import TbMember,TbAdmin,TbBookinfo
from django.core import serializers
import json


def back_index(request):
    ctx={}
    loginname=TbMember.objects.filter(username=str(request.session.get('username', '')))
    if loginname:
        ctx['rlt']=loginname
    elif request.session.get('username',''):
        ctx['rlt'] = request.session.get('username','')
    else:
        ctx['rlt']='请先登录'
    return render(request,'back/index.html',ctx)


def userinfotable(request):
    request.encoding='utf-8'
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword=='userinfo':
            if 'value' in request.GET:
                username = request.GET['value']
                if username:
                    db = TbMember.objects.filter(username=username)
                else:
                    db = TbMember.objects.all()
            else:
                db = TbMember.objects.all()
        elif keyword=='shopinfo':
            if 'value' in request.GET:
                shopname = request.GET['value']
                if shopname:
                    db=TbBookinfo.objects.filter(bookname=shopname)
                else:
                    db=TbBookinfo.objects.all()
            else:
                db=TbBookinfo.objects.all()
    ajax_testvalue = serializers.serialize("json", db)
    m=json.loads(ajax_testvalue)
    data_db=[x['fields'] for x in m]
    data = {"code": 0, "msg": "", "count": 10, "data": data_db}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse(m[0]['fields'])
    #return JsonResponse(m[0]['fields'],safe=False)


def userinfo(request):
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'},{field:'username', width:'8%', title: '用户名', sort: true} \
      ,{field:'password', width:'8%', title: '密码'} \
      ,{field:'email', width:'20%', title: '邮箱'} \
      ,{field:'phonecode', width:'15%', title: '电话'} \
      ,{field:'realname', width:'7%',title:'姓名'} \
      ,{field:'address_sheng', width:'8%',title:'省'} \
      ,{field:'address_shi', width:'10%',title:'市'} \
      ,{field:'address_quxian', width:'10%',title:'区县'} \
      ,{field:'address_detail', width:'20%',title:'详细地址'} \
      ,{fixed: 'right', width: 165, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='userinfo'

    return render(request,'back/userinfo.html',ctx)

def shopinfo(request):
    ctx={}
    ctx['rlt']="[{type:'checkbox',fixed:'true'}\
      ,{field:'bookname', width:'30%', title: '商品名称', sort: true} \
      ,{field:'bookintroduce', width:'20%', title: '商品介绍'} \
      ,{field:'author', width:'10%', title: '作者'} \
      ,{field:'company', width:'15%', title: '出版社'} \
      ,{field:'marketprice', width:'7%',title:'原件'} \
      ,{field:'hotprice', width:'8%',title:'折扣价'} \
      ,{field:'loaddate', width:'10%',title:'出版时间'} \
      ,{fixed: 'right', width: 165, align:'center', toolbar: '#barDemo'}\
    ]"
    ctx['keyword']='shopinfo'

    return render(request,'back/userinfo.html',ctx)

def person_info(request):
    user=request.session.get('username','')
    if user=='':
        return render(request,'wap_login.html')
    else:
        return render(request,'person_info.html')


