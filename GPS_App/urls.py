from . import views,login
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home ,name='home'),
    path('index',views.index,name='index') ,


    path('get_device_locations/', views.get_device_locations, name='get_device_locations'),
    path('get_device_ids/', views.get_device_ids, name='get_device_ids'),
    path('map/', views.show_map, name='map'),


    path('login/',login.login,name='login'),
    path('logout/',login.logout,name='logout'),

    # path('get_device_emergency_alarm',views.get_device_emergency_alarm,name='get_device_emergency_alarm'),
    path('get_device_configs/', views.get_device_configs, name='get_device_configs'),
    path('save_device_configs/', views.save_device_configs, name='save_device_configs'),
    path('get_device_emergency_alarms/', views.get_device_emergency_alarms, name='get_device_emergency_alarms'),
    path('get_device_emergency_alarms_stop/', views.get_device_emergency_alarms_stop, name='get_device_emergency_alarms_stop'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
