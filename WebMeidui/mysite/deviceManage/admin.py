from django.contrib import admin

# Register your models here.
from .models import data, equipment


class dataAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment_id', 'time', 'voltage', 'temperature']


admin.site.register(data, dataAdmin)


class equipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment_id', 'status', ]


admin.site.register(equipment, equipmentAdmin)
