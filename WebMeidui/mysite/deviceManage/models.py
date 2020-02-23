from django.db import models
import time
import re


# Create your models here.
# 创建设备表
class equipment(models.Model):
    STATUS_CHOISE = (
        ('0', '正常'),
        ('1', '异常'),
    )
    id = models.AutoField(primary_key=True, verbose_name='设备主键')
    name = models.CharField(max_length=200, verbose_name='设备名称', null=False,
                            default='设备')
    equipment_id = models.CharField(max_length=200, verbose_name='设备代码', unique=True, null=False)
    status = models.CharField(choices=STATUS_CHOISE, default='0', max_length=2, verbose_name='状态')

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class equipmentAttr(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='属性主键')
    equipment_com = models.CharField(max_length=200, default='COM1', verbose_name='设备串口', )
    equipment_rate = models.CharField(max_length=200, default='9600', verbose_name='设备波特率', )

    class Meta:
        verbose_name = '设备属性'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class warning(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='属性主键')
    temperatureWarning = models.CharField(max_length=20, default='50', verbose_name='温度线', )
    voltageWarning = models.CharField(max_length=20, default='3', verbose_name='电压线', )

    class Meta:
        verbose_name = '报警线'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# 创建返回设备表
class data(models.Model):
    STATUS_TEMPERATURE = (
        ('0', '正常'),
        ('1', '超温'),
    )
    STATUS_VOLTAGE = (
        ('0', '正常'),
        ('1', '电压低'),
    )
    id = models.AutoField(primary_key=True, verbose_name='返回信息主键')
    equipment_id = models.ForeignKey(to=equipment, to_field='id', on_delete=models.CASCADE, verbose_name="设备号")
    time = models.DateTimeField(auto_now_add=True, verbose_name='数据返回时间')
    voltage = models.CharField(max_length=20, verbose_name='设备电压')
    temperature = models.CharField(max_length=20, verbose_name='温度')
    temperature_status = models.CharField(choices=STATUS_TEMPERATURE, default='0', max_length=2, verbose_name='温度状态')
    voltage_status = models.CharField(choices=STATUS_VOLTAGE, default='0', max_length=2, verbose_name='电压状态')

    def save(self, *args, **kwargs):
        myvoltage = float(re.findall('[0-9.]+', self.voltage)[0])
        mytemperature = float(re.findall('[0-9.]+', self.temperature)[0])
        temperatureWarning = float(re.findall('[0-9.]+',warning.objects.all()[0].temperatureWarning)[0])
        voltageWarning = float(re.findall('[0-9.]+',warning.objects.all()[0].voltageWarning)[0])
        print(myvoltage, mytemperature)
        if mytemperature >= temperatureWarning:
            self.temperature_status = '1'
        else:
            self.temperature_status = '0'
        if myvoltage < voltageWarning:
            self.voltage_status = '1'
        else:
            self.voltage_status = '0'
        super(data, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '数据'
        verbose_name_plural = verbose_name
        ordering = ['-time']

    def __str__(self):
        return str(self.id)
