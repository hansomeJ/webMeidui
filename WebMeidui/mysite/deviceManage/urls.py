from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^datas/', views.datas, name='datas'),
    url(r'^set/', views.set, name='set'),
    url(r'^export_excel/', views.export_excel, name='export_excel'),
    url(r'^historyData/(?P<id>\d+)', views.historyData, name='historyData'),
    url(r'^start/', views.start, name='start'),
    url(r'^data_visual/', views.data_visual, name='data_visual'),
    url(r'^warningSet/', views.warningSet, name='warningSet'),
]
