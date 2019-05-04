from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from netstore.database import TbMember, TbBookinfo,Tbcart
from django.core import serializers
import json



def index(request):
    ctx = {}
    if request.GET:
        # 加购物车，状态为：0，待审批为：1，审批完成为：2,
        if request.GET['keyword'] == 'addcart':
            itemid = request.GET['value']
            userid = request.session.get('username', '')[0]['userid']
            carthas = Tbcart.objects.filter(itemid=itemid, approval='0', userid=userid)
            itemname = TbBookinfo.objects.filter(id=itemid)
            if carthas:
                qty = carthas[0]['cartqty']
                cartqty = str(int(qty) + 1)
                Tbcart.objects.filter(itemid=itemid).update(cartqty=cartqty)
            elif Tbcart.objects.filter(approval='0', userid=userid):
                cartid = Tbcart.objects.filter(approval='0', userid=userid)
                addcart = Tbcart(cartid=cartid[0]['cartid'], itemid=itemid, cartname=itemname[0]['itemname'],
                                 cartqty='1', approval='0', price=str(itemname[0]['price_r']),
                                 memberid=itemname[0]['supplier'], userid=userid)
                addcart.save()
            else:
                addcart = Tbcart(cartid='111', itemid=itemid, cartname=itemname[0]['itemname'], cartqty='1',
                                 approval='0', price=str(itemname[0]['price_r']), memberid=itemname[0]['supplier'],
                                 userid=userid)
                addcart.save()
        elif request.GET['keyword']=='shopdetail':
            itemid=request.GET['value']
            return HttpResponseRedirect('/index/')
        elif request.GET['keyword'] == 'quit':
            request.session['username'] = ''
        html_str = 'app/wap_login.html'
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
            html_str = '/wap_login/'
            return HttpResponseRedirect(html_str, ctx)
    ctx['keyword'] = 'shopinfo'
    db = TbBookinfo.objects.all()
    ctx['html1'] = ''
    m = 0
    ctx['id'] = [str(x['id']) for x in db]
    for x in db:
        # ajax_testvalue = serializers.serialize("json", db)
        m += 1
        ctx['html1'] = ctx['html1'] + '<div class="layui-col-xs6">\
          <div class="layui-card">\
            <div class="layui-card-body" style="height: 285px;">\
              <div align="center" style="height: 200px;"><a href="/appdetail/?id='+str(x['id'])+'"><img src="' + x[
            'pic_path'] + '" width="100%" height="100%" onclick="shopdetail(' + str(m) + ')"></a></div>\
                <div class="protxt">\
                  <div class="name" ><b href="/appdetail/?id='+str(x['id'])+'" onclick="shopdetail(' + str(m) + ')">' + x['itemname'] + '</b></div>\
                  <div class="wy-pro-pri">¥<span>' + str(x['price_r']) + '</span></div>\
                </div>\
            </div>\
          </div>\
        </div>'
    ctx['rlt'] = [x['itemname'] for x in db]
    ctx['bookde'] = [y['supplier'] for y in db]
    userid = request.session.get('username', '')[0]['userid']
    itemcart = Tbcart.objects.filter(userid=userid, approval='0')
    confirm=Tbcart.objects.filter(userid=userid, approval='1')
    ctx['cartcount'] = 0
    ctx['confirm']=0
    for n in itemcart:
        ctx['cartcount'] += int(n['cartqty'])
    for m in confirm:
        ctx['confirm']+=int(m['cartqty'])
    ctx['bookpic'] = [str(x['pic_path']) for x in db]
    ctx['price'] = [str(x['price_r']) for x in db]
    return render(request, 'app/index.htm', ctx)