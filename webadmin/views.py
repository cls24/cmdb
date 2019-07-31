from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from repos import models

class AssetManage(View):

    def get(self,req):
        return render(req, 'assetmanage.html')


class AjaxAsset(View):
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
            'text': {'content': '','kwargs':{}},
            'attrs':{}
        },
        {
            'q': 'device_type_id',
            'title': '资产类型',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@@device_type_choices'}},
            'attrs': {'edit': True, 'type': 'select'}
        },
        {
            'q': 'device_status_id',
            'title': '资产状态',
            'display': True,
            'text':{'content': '{n}','kwargs':{'n':'@@device_status_choices'}},
            'attrs': {'edit': True, 'type': 'select'}

        },
        {
            'q': 'Cabinet_num',
            'title': '机架号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@Cabinet_num'}},
            'attrs': {'edit': True, 'type': 'input'}

        },
        {
            'q': 'Cabinet_order',
            'title': '机架中序号',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@Cabinet_order'}},
            'attrs': {'edit': True, 'type': 'input'}

        },
        {
            'q': 'idc',
            'title': 'IDC',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@@idc_choices'}},
            'attrs': {'edit': True, 'type': 'select'}

        },
        {
            'q': 'business_unit',
            'title': '业务线',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@@business_choices'}},
            'attrs': {'edit': True, 'type': 'select'}

        },
        {
            'q': 'department',
            'title': '部门',
            'display': True,
            'text': {'content': '{a}', 'kwargs': {'a': '@@department_choices'}},
            'attrs': {'edit': True, 'type': 'select'}

        },
        {
            'q': 'latest_date',
            'title': '最后更新日期',
            'display': True,
            'text': {'content': '{n}', 'kwargs': {'n': '@latest_date'}},
            'attrs': {'edit': True, 'type': 'input'}

        },
        {
            'q': None,
            'title': '查看',
            'display': True,
            'text':{'content': '<a href="/assetdetail/{id}">{n}</a>','kwargs':{'n':'查看详细','id':'@id'}},
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

        res = models.Asset.objects.all().values(*self.getKeys(self.li))
        return JsonResponse({
            "tb_config": self.li,
            'tb_data':list(res),
            'global_dict':{
                'device_status_choices': models.Asset.device_status_choices,
                'device_type_choices': models.Asset.device_type_choices,
                'idc_choices': list(models.IDC.objects.all().values_list('id','name')),
                'business_choices': list(models.BusinessUnit.objects.all().values_list('id','name')),
                'department_choices': list(models.Department.objects.all().values_list()),
            }
        })

    def post(self, req):
        return JsonResponse("ok")



