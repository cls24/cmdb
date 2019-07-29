from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils import auth



@method_decorator(csrf_exempt, name='dispatch')
class test(View):

    def get(self,req):
        return HttpResponse('')

    @method_decorator(auth.authkey)
    def post(self,req):
        return HttpResponse('ok')

