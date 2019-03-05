from django.shortcuts import render
from django.http import HttpResponse
from netstore.sqldatabase import TbMember,TbAdmin


def back_index(request):
    ctx={}
    ctx['rlt']='chenchen'
    return render(request,'search.html',ctx)