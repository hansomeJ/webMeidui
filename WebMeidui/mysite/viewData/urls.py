from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Echarts/(?P<id>\d+)', views.index, name='echarts'),
]