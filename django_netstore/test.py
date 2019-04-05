from django.shortcuts import render,HttpResponseRedirect
from netstore.database import Tbcart,TbMember
from django.db.models import Count
import simplejson
import json


def test(request):
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
        m=0
        for n in itemcart:
            m+=1
            membernamenow = n['memberid']
            frontqty=n['cartqty']
            cartname=n['cartname']
            if membernamelast==membernamenow:
                membernamenow=membernamelast
            else:
                membername=TbMember.objects.filter(userid=membernamenow)
                ctx['com']=ctx['com']+'<div>\
        <div class="layui-col-md2" align="center">\
        <b>'+membername[0]['realname']+'</b>\
        </div>\
        <hr class="layui-bg-green">'
            ctx['rlt']='<blockquote class="layui-elem-quote" id="'+str(n['id'])+'">\
                <div class="layui-row layui-col-space10">\
              <div class="layui-col-md2" align="center">\
                <img src="upload/123.jpg" height="80" width="80" style="border:1px solid black"/>\
              </div>\
              <div class="layui-col-md4" style="vertical-align:middle">\
                <a>'+cartname+'</a>\
              </div>\
              <div class="layui-col-md4" align="center">\
                  <a>数量:       </a><button class="layui-btn layui-btn-primary layui-btn-sm" onclick="add('+str(m)+')">+</button><input id="'+str(m)+'" type="text" size="2" value="'+frontqty+'" align="center"><button  class="layui-btn layui-btn-primary layui-btn-sm" onclick="del('+str(m)+')">-</button>\
              </div> <div class="layui-col-md2" align="center"><button class="layui-btn layui-btn-danger" onclick="del_item('+str(m)+')">删除商品</button></div>\
            </div></blockquote><hr>'
            ctx['com'] = ctx['com'] + ctx['rlt']
            ctx['foot']='</div>\
            </div>\
            <br>'
            ctx['com']=ctx['com']+ctx['foot']
            ctx['rlt']=''
            ctx['foot']=''

        '''
        if request.POST['name']=='delete':
            poststr['id']=request.POST['id']
            Tbcart.objects.filter(cartid=poststr['id']).delete()
        elif request.POST['name']=='submit':
            poststr['id']=request.POST['id']
            poststr['qty']=request.POST['qty']
    '''

        return render(request,'cart.html',ctx)


