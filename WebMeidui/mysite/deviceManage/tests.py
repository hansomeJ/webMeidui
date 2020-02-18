from django.test import TestCase

# Create your tests here.
from deviceManage.models import data

all = data.objects.all()
for i in all :
    i.save()