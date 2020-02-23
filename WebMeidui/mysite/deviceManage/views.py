from django.shortcuts import render
from .models import equipment, data, equipmentAttr,warning
import serial
import math
import time
import threading
import pyecharts
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.faker import Faker
from django.template import loader
from pyecharts.charts import Line3D
# from pyecharts.constants import DEFAULT_HOST
from mysite.connect import Data
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from mysite.settings import STATICFILES_DIRS
import xlwt
from io import BytesIO, StringIO
import codecs, os
from datetime import timezone
from datetime import timedelta

# device1 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])
# device2 = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])

# device1.start()
# device2.start()

# Create your views here.
'''
分页功能
'''
def my_page(data, pagenum):
    #设置每页显示数据的条数
    paginator = Paginator(object_list=data, per_page=4)
    # 生成一个page对象
    page = paginator.page(pagenum)
    return page

'''

'''
def index(request):
    device = equipment.objects.all()#从数据库中获取所有的设备信息
    eq = equipmentAttr.objects.all()[0]#从数据库中获取设备属性第一条数据
    war =warning.objects.all()[0]
    if request.method == 'GET':
        return render(request, 'deviceManage/index.html', {'device': device, 'eq': eq,'war':war})
        # C08A031A17FC,25.06C,3.296V
    else:
        deviceList = []
        for i in request.POST.values():#获取前端提交的设备号
            try:
                int(i)
                dec = equipment.objects.get(pk=i)#根据设备编号获取设备对象
                # print(dec.name)
                deviceList.append(dec)

            except:
                pass
        return render(request, 'deviceManage/index.html', {'device': device, 'devices': deviceList, 'eq': eq,'war':war})

'''
通过JS定时向后端请求数据
'''
@require_POST
@csrf_exempt
def datas(request):
    id = request.POST.get('ids')#从前端获取设备id
    device = equipment.objects.get(pk=id)#通过设备id查询设备信息
    equipmentData = data.objects.filter(equipment_id=device)#通过设备id从数据表中筛选数据
    dataTime = equipmentData[0].time.astimezone(timezone(timedelta(hours=+8))).strftime("%Y-%m-%d %H:%M:%S")
    voltage = equipmentData[0].voltage
    temperature = equipmentData[0].temperature
    temperature_status = equipmentData[0].temperature_status
    voltage_status = equipmentData[0].voltage_status
    status = device.status
    if status == '0':
        status = '正常'
    else:
        status = '异常'
    result = {'deviceId': id, 'dataTime': dataTime, 'voltage': voltage, 'temperature': temperature,
              'temperature_status': temperature_status, 'voltage_status': voltage_status, 'Success': 'ok',
              'status': status}
    return JsonResponse(result)

'''
唤醒硬件
'''
@require_POST
@csrf_exempt
def start(request):
    id = request.POST.get('ids')
    device = equipment.objects.get(pk=id)
    equipmentattr = equipmentAttr.objects.all()[0]
    com = equipmentattr.equipment_com
    rate = equipmentattr.equipment_rate
    equipment_id = device.equipment_id
    print(equipment_id)
    # 0x8A,0x05,0x17,0x11,0x11
    mylist = equipment_id.split(',')
    myequipment = Data(com, rate, mylist)
    myequipment.start()
    result = {'Success': 'ok'}
    return JsonResponse(result)

'''
设置串口和波特率
'''
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

'''
查看历史数据
'''
def historyData(request, id):
    pagenum = request.GET.get('page', None)#从前端获取要查看的页码
    device = equipment.objects.get(pk=id)#获取设备对象
    # 如果当前页数为None 则pagenum的值为1
    pagenum = 1 if pagenum == None else pagenum

    # 根据设备筛选历史数据
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
    sheet.write(0, 3, u'电压状态')
    sheet.write(0, 4, u'温度状态')


    # 写入数据
    data_row = 1

    for i in datas:
        # 格式化datetime
        time = i.time.strftime("%Y-%m-%d %H:%M:%S")
        if i.temperature_status == '0':
            temperature='正常'
        else:
            temperature = '超温'
        if i.voltage_status == '0':
            voltage = "正常"
        else:
            voltage = "电压低"
        sheet.write(data_row, 0, i.voltage)
        sheet.write(data_row, 1, i.temperature)
        sheet.write(data_row, 2, time)
        sheet.write(data_row, 3, voltage)
        sheet.write(data_row, 4, temperature)

        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    file = 'static/dataFile/' + filename
    wb.save(file)
    # 重新定位到开始
    output.seek(0)
    return JsonResponse({'file': file,'filename':filename})

# 数据可视化

def data_visual(request):
    template = loader.get_template('deviceManage/Echarts.html')
    l3d = line3d()
    context = dict(
        myechart=l3d.render_embed(),
        host=443,
        script_list=l3d.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo")
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d

@require_POST
@csrf_exempt
def warningSet(request):
    temperatureWarning = request.POST.get('temperatureWarning',None)
    voltageWarning = request.POST.get('voltageWarning',None)
    print(temperatureWarning,voltageWarning)
    if temperatureWarning and voltageWarning is not None:
        war = warning.objects.all()[0]
        war.temperatureWarning=temperatureWarning
        war.voltageWarning=voltageWarning
        war.save()
        datas = data.objects.all()
        for i in datas:
            i.save()
        return JsonResponse({'Success': 'ok'})
    return JsonResponse({'Success': 'error'})