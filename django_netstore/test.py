from django.shortcuts import render,HttpResponse


def test(request):
    clx=[]
    if request.method == 'POST':# 获取对象
        obj = request.FILES.get('upload')
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        f = open(os.path.join(BASE_DIR, 'upload', 'pic', obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('OK'+'upload/pic/'+obj.name)

    return render(request, 'test.html')

