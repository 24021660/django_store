from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from netstore.sqldatabase import TbMember,TbAdmin
from django.core import serializers
import json

def back_index(request):
    ctx={}
    ctx['rlt']='chenchen'
    return render(request,'back_index.html',ctx)

def test(request):


    db = TbMember.objects.all()
    ajax_testvalue = serializers.serialize("json", db)
    data = {"code": 0, "msg": "", "count": 10, "data": ajax_testvalue}
    #return HttpResponse(json.dumps(db), content_type="application/json")

    return HttpResponse(ajax_testvalue)

