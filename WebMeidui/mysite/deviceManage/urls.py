from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/', views.index,name='index'),
    url(r'^datas/', views.datas,name='datas'),
]