
from django.urls import path
from  webadmin import views

urlpatterns = [
    path('asset',views.Asset.as_view()),
    path('assetjson',views.AssetJson.as_view()),
    path('server',views.Server.as_view()),
    path('serverjson',views.ServerJson.as_view()),
]
