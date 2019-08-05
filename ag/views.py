from django.shortcuts import render,HttpResponse

# Create your views here.

def test(req):

    return HttpResponse('ok')