from repos import models
import json,math
from utils.pager import Pager
"""
    Server = models.OneToOneField('Server', on_delete=models.CASCADE)
    hostname = models.CharField('主机名', max_length=128, unique=True)
    sn = models.CharField('sn号', max_length=64, db_index=True)
    vendor = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64,null=True, blank=True)
    manage_ip = models.GenericIPAddressField('管理ip', null=True, blank=True)
    os_platform = models.CharField('系统平台', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)
    cpu_model = models.CharField('型号', max_length=64)
    cpu_cores = models.IntegerField('核数')
    add_time = models.DateTimeField(auto_now_add=True)
"""
class ServerJson():
    tb_config = [
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {'content': '', 'kwargs': {}},
            'attrs': {}
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {'content': 'n','kwargs':{'n':'@id'}},
            'attrs':{}
        },
        {
            'q': 'asset_id',
            'title': '资产号',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@asset_id'}},
            'attrs': {'edit': False, 'type': 'select','newvalue':'','oldvalue':'@asset_id'}
        },
        {
            'q': 'hostname',
            'title': '主机名',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@hostname'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@hostname'}
        },
        {
            'q': 'sn',
            'title': 'sn号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@sn'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@sn'}

        },
        {
            'q': 'vendor',
            'title': '制造商',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@vendor'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@vendor'}
        },
        {
            'q': 'model',
            'title': '型号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@model'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@model'}
        },
        {
            'q': 'manage_ip',
            'title': '管理ip',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@manage_ip'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@manage_ip'}
        },
        {
            'q': 'os_platform',
            'title': '系统平台',
            'display': True,
            'text': {'content': '{a}', 'kwargs': {'a': '@os_platform'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@os_platform'}
        },
        {
            'q': 'os_version',
            'title': '系统版本',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@os_version'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@os_version'}
        },
        {
            'q': 'cpu_model',
            'title': 'cpu',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@cpu_model'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@cpu_model'}
        },
        {
            'q': 'cpu_cores',
            'title': 'cpu核数',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@cpu_cores'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@cpu_cores'}
        },
        {
            'q': 'os_version',
            'title': '系统版本',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@os_version'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@os_version'}
        },
        {
            'q': 'add_time',
            'title': '更新时间',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@add_time'}},
            'attrs': {'edit': False, 'type': 'input', 'newvalue': '', 'oldvalue': '@add_time'}
        },
        {
            'q': None,
            'title': '查看',
            'display': True,
            'text':{'content': '<a href="/serverdetail/{id}">{n}</a>','kwargs':{'n':'详细','id':'@id'}},
            'attrs':{}
        },
    ]

    def get(self, req):
        pn = req.GET.get('pn')
        current_page = int(pn)
        per_page = 10
        pg_num = 5
        res = models.Server.objects.all().values(*[i['q'] for i in self.tb_config if i['q']])
        total_pg = math.ceil(len(res)/per_page)
        pager = Pager.makePager(pg_num, current_page, total_pg)
        data = {
            "tb_config": self.tb_config,
            'tb_data':list(res[per_page*(current_page-1):per_page*current_page]),
            'pager':pager,
            'global_dict':{
                # 'asset_id': list(models.Asset.objects.all().values_list('id','name')),
            }
        }
        return data

    def post(self, req):
        data = json.loads(req.POST.get('data'))
        resp = {"status":True,"err":"","msg":""}
        try:
            for k,v in data.items():
                models.Server.objects.filter(id=k).update(**v)
        except Exception as e:
            resp['status'] = False
            resp['err'] = e.__str__()
        return resp