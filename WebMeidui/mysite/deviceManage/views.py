from django.shortcuts import render
from .models import equipment, data, equipmentAttr
import serial
import time
import threading
from mysite.connect import Data
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.http import JsonResponse, HttpResponse


# device1 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])
# device2 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])

# device1.start()
# device2.start()

# Create your views here.
def index(request):
    device = equipment.objects.all()
    eq = equipmentAttr.objects.all()[0]
    if request.method == 'GET':
        return render(request, 'deviceManage/index.html', {'device': device, 'eq': eq})
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
        return render(request, 'deviceManage/index.html', {'device': device, 'devices': deviceList, 'eq': eq})


@require_POST
@csrf_exempt
def datas(request):
    id = request.POST.get('ids')
    device = equipment.objects.get(pk=id)
    equipmentData = data.objects.filter(equipment_id=device)
    dataTime = equipmentData[0].time.strftime("%Y-%m-%d %H:%M:%S")
    voltage = equipmentData[0].voltage
    temperature = equipmentData[0].temperature
    status = device.status
    if status == '0':
        status = '正常'
    else:
        status = '异常'
    result = {'deviceId': id, 'dataTime': dataTime, 'voltage': voltage, 'temperature': temperature, 'Success': 'ok',
              'status': status}
    return JsonResponse(result)


@require_POST
@csrf_exempt
def set(request):
    com = request.POST.get('com', None)
    rate = request.POST.get('rate', None)
    if com is not None:
        try:
            eq = equipmentAttr.objects.all()[0]
            eq.equipment_com = com
            eq.save()
            return JsonResponse({'Success': 'ok', 'com': eq.equipment_com})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'setting com error!'})
    if rate is not None:
        try:
            eq = equipmentAttr.objects.all()[0]
            eq.equipment_rate = rate
            eq.save()
            return JsonResponse({'Success': 'ok', 'rate': eq.equipment_rate})
        except Exception as e:
            print(e)
            return JsonResponse({'Error': 'setting com error!'})


# 显示设备界面
def selectEquipment(request, id):
    pass

# 数据接收界面
