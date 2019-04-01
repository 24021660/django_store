"""django_netstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
from . import login_register,back_index,forms,test
from django_netstore.wx import wx
from django.views.static import serve
from django_netstore.settings import MEDIA_ROOT
urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^static/(?P<path>.*)',static.serve,({'document_root':os.path.join(BASE_DIR,'upload')})),
    url(r'^wap/$', login_register.login),
    url(r'^register/$', login_register.register),
    url(r'^index/$', back_index.back_index),
    url(r'^userinfotable/', back_index.userinfotable),
    url(r'^userinfo/', back_index.userinfo),
    url(r'^test/', forms.tabletest),
    url(r'^test$',test.test),
    url(r'^shopinfo$',back_index.shopinfo),
    url(r'^shoplist$',back_index.shoplist),
    url(r'^itemadd',back_index.shopadd),
    url(r'^upload/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    url(r'^memadd',login_register.addmember),
    url(r'^wx$', wx.weixin_main),
    ]
