
from django.urls import path
from  webadmin import views

urlpatterns = [
    path('assetjson',views.AssetJson.as_view()),
    path('asset',views.Asset.as_view()),
]
