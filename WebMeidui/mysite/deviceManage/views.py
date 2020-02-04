from django.shortcuts import render
from .models import equipment, data
import serial
import time
import threading
from mysite.connect import Data


# device1 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])
# device2 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])

# device1.start()
# device2.start()

# Create your views here.
def index(request):
    device = equipment.objects.all()
    if request.method == 'GET':
        return render(request, 'deviceManage/index.html', {'device': device})
        # C08A031A17FC,25.06C,3.296V
    else:
        deviceList = []
        for i in request.POST.values():
            try:
                int(i)
                dec = equipment.objects.get(pk=i)
                deviceList.append(dec)

            except:
                pass
        return render(request, 'deviceManage/index.html', {'device': device, 'devices': deviceList})


# 显示设备界面
def selectEquipment(request, id):
    pass

# 数据接收界面
