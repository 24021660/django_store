from django.shortcuts import render,HttpResponseRedirect
from netstore.database import TbMember
from django.core import serializers


def login(request):
    ctx = {}
    html_str = 'login.html'
    if request.POST:
        username=request.POST['login_username'].strip()
        password=request.POST['login_password'].strip()
        if username=='' or password=='':
            ctx['rlt']='用户名或密码不能为空'
        else:
            usernamedb=TbMember.objects.filter(username=username,password=password)
            if usernamedb:
                lendb = len(usernamedb)
                data_db = []
                
                for m in range(0, lendb):  #判断是否为n和2，用于跳转完善信息界面
                    fields = {}
                    for n in usernamedb[m]:
                        if n == 'id':
                            continue
                        fields[n] = usernamedb[m][n]
                    data_db.append(fields)
                if data_db[0]['is_used']=='n' and data_db[0]['level']=='2':
                    html_str='/register/'
                    request.session['username'] = data_db
                    return HttpResponseRedirect(html_str, ctx)
                else:
                    request.session['username']=data_db
                    if request.session['username']:
                        ctx['rlt']=username
                        html_str = '/index/'
                        return HttpResponseRedirect(html_str, ctx)
                    else:
                        ctx['rlt']='登录失败'
            else:
                ctx['rlt']='登录失败'
    else:
        ctx['rlt'] = '请输入用户名和密码'
    return render(request,html_str,ctx)


def addmember(request):
    ctx={}
    ctx['rlt']='请输入用户名和密码'
    if request.POST:
        username=request.POST['register_username'].strip()
        password=request.POST['register_password'].strip()
        if username == '' or password == '':
            ctx['rlt'] = '请输入用户名/密码/邮箱'
        else:
            is_member = TbMember.objects.filter(username=username)
            if is_member:
                ctx['rlt']='用户名已存在'
            else:
                member=TbMember(username=username,password=password,is_used='n',level='0')
                member.save()
                ctx['rlt'] = '用户创建成功'
    return render(request,'back/add_member.html',ctx)

def addmember2(request):
    ctx={}
    ctx['rlt']='请输入用户名和密码'
    if request.POST:
        username=request.POST['register_username'].strip()
        password=request.POST['register_password'].strip()
        if username == '' or password == '':
            ctx['rlt'] = '请输入用户名/密码/邮箱'
        else:
            is_member = TbMember.objects.filter(username=username)
            if is_member:
                ctx['rlt']='用户名已存在'
            else:
                member=TbMember(username=username,password=password,is_used='n',level='1')
                member.save()
                ctx['rlt'] = '用户创建成功'
    return render(request,'back/add_manage.html',ctx)


def register(request):
    ctx={}
    html_str='register.html'
    if request.POST:
        username=request.session.get('username', '')[0]['username']
        realname=request.POST['register_username'].strip()
        password=request.POST['register_password'].strip()
        re_email=request.POST['register_email']
        phone=request.POST['register_phone']
        password1 = request.POST['confirm_password'].strip()
        people = request.POST['register_people'].strip()
        register_id=request.POST['register_id'].strip()
        detail=request.POST['register_detail'].strip()
        logo=request.FILES.get('register_logo')
        obj = request.FILES.get('upload')
        #address=request.POST['register_address']
        if username=='' or password==''or re_email=='':
            ctx['rlt']='请输入用户名/密码/邮箱'
        else:
            is_member=TbMember.objects.filter(realname=realname)
            if is_member:
                ctx['rlt'] = '该用户已存在'
            else:
                member=TbMember.objects.filter(username=username).update(realname=realname,password=password,email=re_email,phonecode=phone,duty_people=people,userid=register_id,register_pic='upload/menberpic/'+obj.name,is_used='y',detail=detail,logo='upload/menberlogo/'+logo.name)
                is_member=TbMember.objects.filter(userid=register_id)
                if is_member:
                    import os
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    f = open(os.path.join(BASE_DIR, 'upload', 'memberpic', register_id), 'wb')
                    for chunk in obj.chunks():
                        f.write(chunk)
                    f.close()
                    l = open(os.path.join(BASE_DIR, 'upload', 'memberlogo', register_id), 'wb')
                    for chunk in logo.chunks():
                        l.write(chunk)
                    l.close()
                ctx['rlt']='用户注册成功！'
                html_str='/wap/'
                return HttpResponseRedirect(html_str, ctx)
    else:
        ctx['rlt']='post失败'
    return render(request,html_str,ctx)


def wap_login(request):
    ctx = {}
    html_str = 'app/wap_login.html'
    if request.POST:
        username = request.POST['login_username'].strip()
        password = request.POST['login_password'].strip()
        if username == '' or password == '':
            ctx['rlt'] = '用户名或密码不能为空'
        else:
            usernamedb = TbMember.objects.filter(username=username, password=password)
            if usernamedb:
                lendb = len(usernamedb)
                data_db = []

                for m in range(0, lendb):  # 判断是否为n和2，用于跳转完善信息界面
                    fields = {}
                    for n in usernamedb[m]:
                        if n == 'id':
                            continue
                        fields[n] = usernamedb[m][n]
                    data_db.append(fields)
                if data_db[0]['is_used'] == 'n' and data_db[0]['level'] == '2':
                    html_str = '/register/'
                    request.session['username'] = data_db
                    return HttpResponseRedirect(html_str, ctx)
                else:
                    request.session['username'] = data_db
                    if request.session['username']:
                        ctx['rlt'] = username
                        html_str = '/wap_index'
                        return HttpResponseRedirect(html_str, ctx)
                    else:
                        ctx['rlt'] = '登录失败'
            else:
                ctx['rlt'] = '登录失败'
    else:
        ctx['rlt'] = '请输入用户名和密码'
    return render(request, html_str, ctx)