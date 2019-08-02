from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from webadmin.services import asset

class Asset(View):
    def get(self,req):
        return render(req, 'web/asset.html')

class AssetJson(View):
    asset = asset.AssetJson()
    def get(self, req):
        return JsonResponse(self.asset.get(req))

    def post(self, req):
        return JsonResponse(self.asset.post(req))




