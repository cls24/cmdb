
from django.urls import path,re_path
from api import views
urlpatterns = [
    re_path(r'\w{32}$',views.test.as_view())
]
