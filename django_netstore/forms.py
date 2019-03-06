from django.shortcuts import render
from django.http import HttpResponse
from netstore.sqldatabase import TbMember,TbAdmin


def test(request):
    return render(request,'search.html')