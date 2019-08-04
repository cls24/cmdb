from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from webadmin.services import asset,server


class Asset(View):
    def get(self,req):

        return render(req, 'web/asset.html')

class AssetJson(View):
    asset = asset.AssetJson()
    def get(self, req):
        return JsonResponse(self.asset.get(req))

    def post(self, req):
        return JsonResponse(self.asset.post(req))


class Server(View):
    def get(self,req):
        return render(req,'web/server.html')

class ServerJson(View):
    server = server.ServerJson()
    def get(self, req):
        return JsonResponse(self.server.get(req))

    def post(self, req):
        return JsonResponse(self.server.post(req))