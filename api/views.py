from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils import auth
from django.http.response import JsonResponse
from api.services import assetapi
@method_decorator(csrf_exempt, name='dispatch')
class test(View):

    @method_decorator(auth.authkey)
    def post(self,req):
        resp = assetapi.AssetApi().post(req)
        return JsonResponse(resp)

