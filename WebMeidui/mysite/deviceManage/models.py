from django.db import models
import time


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


# 创建返回设备表
class data(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='返回信息主键')
    equipment_id = models.ForeignKey(to=equipment, to_field='id', on_delete=models.CASCADE, verbose_name="设备号")
    time = models.DateTimeField(auto_now_add=True, verbose_name='数据返回时间')
    voltage = models.CharField(max_length=20, verbose_name='设备电压')
    temperature = models.CharField(max_length=20, verbose_name='温度')

    class Meta:
        verbose_name = '数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
