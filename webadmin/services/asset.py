from repos import models
import json

class AssetJson():
    li = [
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
            'q': 'device_type_id',
            'title': '资产类型',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@@device_type_id'}},
            'attrs': {'edit': True, 'type': 'select','newvalue':'','oldvalue':'@@device_type_id'}
        },
        {
            'q': 'device_status_id',
            'title': '资产状态',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@@device_status_id'}},
            'attrs': {'edit': True, 'type': 'select', 'newvalue': '', 'oldvalue': '@@device_status_id'}
        },
        {
            'q': 'Cabinet_num',
            'title': '机架号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@Cabinet_num'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@Cabinet_num'}

        },
        {
            'q': 'Cabinet_order',
            'title': '机架中序号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@Cabinet_order'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@Cabinet_order'}
        },
        {
            'q': 'idc_id',
            'title': 'IDC',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@@idc_id'}},
            'attrs': {'edit': True, 'type': 'select', 'newvalue': '', 'oldvalue': '@@idc_id'}
        },
        {
            'q': 'business_unit_id',
            'title': '业务线',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@@business_unit_id'}},
            'attrs': {'edit': True, 'type': 'select', 'newvalue': '', 'oldvalue': '@@business_unit_id'}
        },
        {
            'q': 'department_id',
            'title': '部门',
            'display': True,
            'text': {'content': '{a}', 'kwargs': {'a': '@@department_id'}},
            'attrs': {'edit': True, 'type': 'select', 'newvalue': '', 'oldvalue': '@@department_id'}
        },
        {
            'q': 'latest_date',
            'title': '最后更新日期',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@latest_date'}},
            'attrs': {'edit': True, 'type': 'input', 'newvalue': '', 'oldvalue': '@latest_date'}
        },
        {
            'q': None,
            'title': '查看',
            'display': True,
            'text':{'content': '<a href="/assetdetail/{id}">{n}</a>','kwargs':{'n':'详细','id':'@id'}},
            'attrs':{}
        },
    ]
    def getKeys(self,li):
        l = []
        for i in li:
            if i['q']:
                l.append(i['q'])
        return l


    def get(self, req):
        pn = req.GET.get('pn')
        current_page = pn if pn else 1
        print(pn)
        res = models.Asset.objects.all().values(*self.getKeys(self.li))
        data = {
            "tb_config": self.li,
            'tb_data':list(res),
            'page_range':(1,6),
            'current_page':1,
            'total_page':10,
            'global_dict':{
                'device_status_id': models.Asset.device_status_choices,
                'device_type_id': models.Asset.device_type_choices,
                'idc_id': list(models.IDC.objects.all().values_list('id','name')),
                'business_unit_id': list(models.BusinessUnit.objects.all().values_list('id','name')),
                'department_id': list(models.Department.objects.all().values_list()),
            }
        }
        return data

    def post(self, req):
        data = json.loads(req.POST.get('data'))
        print(data)
        resp = {"status":True,"err":"","msg":""}
        try:
            for k,v in data.items():
                models.Asset.objects.filter(id=k).update(**v)
        except Exception as e:
            resp['status'] = False
            resp['err'] = e.__str__()
        return resp