from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils import auth
import json
from repos import models

@method_decorator(csrf_exempt, name='dispatch')
class test(View):

    def get(self,req):
        return HttpResponse('')

    @method_decorator(auth.authkey)
    def post(self,req):
        data = json.loads(req.POST.get('data'))
        print(data)
        for host in data.keys():
            server = data[host]['server']
            if server['status']:
                server_data = server['data']
                server_model = models.Server.objects.filter(hostname=host)
                if server_model.exists():
                    del server_data['hostname']
                    print(server_data)
                    server_model.update(**server_data)
                else:
                    asset = models.Asset()
                    asset.save()
                    print(asset.id)
                    server_data['asset']=asset
                    models.Server.objects.create(**server_data)

        return HttpResponse('ok')

