from django.contrib import admin

# Register your models here.
from .models import data, equipment, equipmentAttr, warning


class dataAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment_id', 'time', 'voltage', 'temperature', 'temperature_status', 'voltage_status']


admin.site.register(data, dataAdmin)


class equipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment_id', 'status', ]


admin.site.register(equipment, equipmentAdmin)


class equipmentAttrAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment_com', 'equipment_rate', ]


admin.site.register(equipmentAttr, equipmentAttrAdmin)


class warningAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperatureWarning', 'voltageWarning', ]


admin.site.register(warning, warningAdmin)
