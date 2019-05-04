from . import forms
from netstore.models import User
from django.shortcuts import render_to_response

def register(request):
    if request.method == "POST":
        uf= forms.UserForm(request.POST)
        if uf.is_valid():
            username=(request.POST.get('username')).strip()
            password=(request.POST.get('password')).strip()
            email=(request.POST.get('email')).strip()
            user_list=User.objects.filter(username=username)
            if user_list:
                return render_to_response('register.html',{'uf':uf,'error':'用户名已经存在'})
            else:
                user=User()
                user.username=username
                user.password=password
                user.email=email
                user.save()
                uf.LoginForm()
                return render_to_response('login.html',{'uf':uf})
    else:
        uf= forms.UserForm()
    return render_to_response('register.html',{'uf':uf})

