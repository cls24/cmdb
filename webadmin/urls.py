
from django.urls import path
from  webadmin import views

urlpatterns = [
    path('ajaxasset',views.AjaxAsset.as_view()),
    path('asset',views.AssetManage.as_view())
]
