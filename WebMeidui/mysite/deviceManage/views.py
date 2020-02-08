from django.shortcuts import render
from .models import equipment, data, equipmentAttr
import serial
import time
import threading
from mysite.connect import Data
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from mysite.settings import STATICFILES_DIRS
import xlwt
from io import BytesIO, StringIO
import codecs, os


# device1 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])
# device2 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])

# device1.start()
# device2.start()

# Create your views here.
def my_page(data, pagenum):
    paginator = Paginator(object_list=data, per_page=4)
    # 生成一个page对象
    page = paginator.page(pagenum)
    return page


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


def historyData(request, id):
    pagenum = request.GET.get('page', None)
    device = equipment.objects.get(pk=id)
    # 如果当前页数为None 则pagenum的值为1
    pagenum = 1 if pagenum == None else pagenum

    # 如果年份和月份都不为空的话就按照获取的年份与月份来查询文章
    datas = data.objects.filter(equipment_id=device)

    page = my_page(datas, pagenum)
    return render(request, 'deviceManage/historyData.html', {'page': page, 'device': device})


# 导出excel数据
@require_POST
@csrf_exempt
def export_excel(request):
    id = request.POST.get('id')
    device = equipment.objects.get(pk=id)
    datas = data.objects.filter(equipment_id=device)
    filename = device.name + '.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='gbk')
    # 创建一个sheet对象
    sheet = wb.add_sheet(u"第一页")
    # 写入文件标题
    sheet.write(0, 0, u'电压')
    sheet.write(0, 1, u'温度')
    sheet.write(0, 2, u'时间')

    # 写入数据
    data_row = 1

    for i in datas:
        # 格式化datetime
        time = i.time.strftime("%Y-%m-%d %H:%M:%S")
        sheet.write(data_row, 0, i.voltage)
        sheet.write(data_row, 1, i.temperature)
        sheet.write(data_row, 2, time)
        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    file = 'static/dataFile/' + filename
    wb.save(file)
    # 重新定位到开始
    output.seek(0)
    return JsonResponse({'file': file})
