from django.shortcuts import render,HttpResponse
from netstore.database import Tbcart,TbMember
from django.db.models import Count
def test(request):
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
        membernamenow=n['memberid']
        membernamenow = n['memberid']
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
            <a>微星(msi)GS65 15.6英寸窄边框轻薄游戏本笔记本电脑(i7-8750H 8G*2 256G SSD GTX1060 6G独显 144Hz 黑)</a>\
          </div>\
          <div class="layui-col-md4" align="center">\
              <a>数量:       </a><button class="layui-btn layui-btn-primary layui-btn-sm" onclick="add('+str(m)+')">+</button><input id="'+str(m)+'" type="text" size="2" value="1" align="center"><button  class="layui-btn layui-btn-primary layui-btn-sm" onclick="del('+str(m)+')">-</button>\
          </div> <div class="layui-col-md2" align="center"><button class="layui-btn layui-btn-danger">删除商品</button></div>\
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


