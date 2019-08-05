
from django.contrib import admin
from django.urls import path,include
from cmdb import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('api/', include('api.urls')),
    path('web/', include('webadmin.urls')),
    path('web/', include('ag.urls')),
]
