from django.shortcuts import render,HttpResponse
import json
from netstore.database import TbBookinfo
# Create your tests here.
def tabletest(request):
    db = TbBookinfo.objects()
    #lendb = len(db)
    # ajax_testvalue = serializers.serialize("json", db)
    # m=json.loads(ajax_testvalue)
    lendb = len(db)
    # ajax_testvalue = serializers.serialize("json", db)
    # m=json.loads(ajax_testvalue)
    data_db = []
    for m in range(0, lendb):
        fields = {}
        for n in db[m]:
            if n == 'id':
                continue
            fields[n] = db[m][n]
        data_db.append(fields)
    data = {"code": 0, "msg": "", "count": 1, "data": data_db}

    return HttpResponse(json.dumps(data), content_type="application/json")