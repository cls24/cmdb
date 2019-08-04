from repos import models
import json

class AssetApi():

    def updateOrCreateServer(self,host,server_obj):
        server = server_obj['server']
        if server['status']:
            server_data = server['data']
            server_model = models.Server.objects.filter(hostname=host)
            print(server_data)
            if server_model.exists():
                server_model.update(**server_data)
                return server_model.first().id
            else:
                asset = models.Asset()
                asset.save()
                server_data['asset'] = asset
                s = models.Server.objects.create(**server_data)
                return s.id
        else:
            return None

    def updateOrCreatePlugin(self,plugin,plugin_obj,server_id):
        print(server_id)
        plugin_model = None
        compare_field = None
        data = plugin_obj['data']
        if plugin == 'mem':
            plugin_model = models.Memory
            compare_field = 'slot'
        elif plugin == 'nic':
            plugin_model = models.Nic
            compare_field = 'hwaddr'
        if plugin_model:
            if plugin_obj['status']:
                plugin_model.objects.filter(server=server_id).delete()
                obj_list = []
                for i in data:
                    i['server_id'] = server_id
                    obj_list.append(plugin_model(**i))
                plugin_model.objects.bulk_create(obj_list)
            else:
                pass
        else:
            pass

    def post(self,req):
        data = json.loads(req.POST.get('data'))
        print(data)
        resp = {'status':True,'err':{},'msg':''}

        for host,server_obj in data.items():
            server_id = self.updateOrCreateServer(host,server_obj)
            if  server_id:
                for plugin,plugin_obj in server_obj.items():
                    if plugin != 'server':
                        self.updateOrCreatePlugin(plugin,plugin_obj,server_id)
            else:
                resp['status'] = False
                resp['err']['host'] = False
        return  resp