from django.contrib import admin
from .models import device_logs,user,deviceconfig
# Register your models here.

@admin.register(device_logs)
class device_logs(admin.ModelAdmin):
    list_display = ['id', 'current_device','current_packet_number', 'device_id', 'pckt_id', 'latitude', 'longitude','date','time','pckt_no','created_at','actual_date_time','is_sound_play']


@admin.register(user)
class device_logs(admin.ModelAdmin):
    list_display = ['id', 'first_name','last_name', 'email', 'password', 'mobile', 'image','created_at','updated_at']

@admin.register(deviceconfig)
class deviceconfig(admin.ModelAdmin):
    list_display = ['id', 'device_id','color', 'is_active', 'created_at', 'updated_at']