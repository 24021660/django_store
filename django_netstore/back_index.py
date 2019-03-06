from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from netstore.sqldatabase import TbMember,TbAdmin
from django.core import serializers
import json

def back_index(request):
    ctx={}
    ctx['rlt']='chenchen'
    return render(request,'back/index.html',ctx)


def userinfotable(request):

    db = TbMember.objects.all()
    ajax_testvalue = serializers.serialize("json", db)
    m=json.loads(ajax_testvalue)
    data_db=[x['fields'] for x in m]
    data = {"code": 0, "msg": "", "count": 10, "data": data_db}
    return HttpResponse(json.dumps(data), content_type="application/json")
    #return HttpResponse(m[0]['fields'])
    #return JsonResponse(m[0]['fields'],safe=False)
def userinfo(request):
    return render(request,'back/userinfo.html')
