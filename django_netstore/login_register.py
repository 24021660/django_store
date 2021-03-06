from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,response
from netstore.sqldatabase import TbMember,TbAdmin
from django.core import serializers


def login(request):
    ctx = {}
    html_str = 'wap_login.html'
    if request.POST:
        username=request.POST['login_username'].strip()
        password=request.POST['login_password'].strip()
        if username=='' or password=='':
            ctx['rlt']='用户名或密码不能为空'
        else:
            usernamedb=TbMember.objects.filter(username=username,password=password)
            if usernamedb:
                request.session['username']=serializers.serialize("json", usernamedb)
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


def register(request):
    ctx={}
    html_str='register.html'
    if request.POST:
        username=request.POST['register_username'].strip()
        password=request.POST['register_password'].strip()
        re_email=request.POST['register_email']
        phone=request.POST['register_phone']
        address=request.POST['register_address']
        if username=='' or password==''or re_email=='':
            ctx['rlt']='请输入用户名/密码/邮箱'
        else:
            is_member=TbMember.objects.filter(username=username)
            if is_member:
                ctx['rlt'] = '该用户已存在'
            else:
                member=TbMember(username=username,password=password,email=re_email,phonecode=phone)
                member.save()
                ctx['rlt']='用户注册成功！'
                html_str='registersucess.html'
    else:
        ctx['rlt']='post失败'
    return render(request,html_str,ctx)