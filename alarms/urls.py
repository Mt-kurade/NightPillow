from django.urls import path, include
from .import views 

app_name = 'alarms'

urlpatterns = [
    path('', views.login_views, name='login'),
    path('save_sleep_data/', views.save_sleep_data, name='save_sleep_data'),
    path('sleep_data/', views.sleep_data, name='sleep_data'),
    path('alarms/home/', views.home, name='home'),  
    path('signup/', views.signup, name='signup'),
    path('sleep_calculator/', views.sleep_calculator, name='sleep_calculator'),
    path("save-sleep-data/", views.save_sleep_data, name="save_sleep_data"),
    path("reminders/", views.reminders, name="reminders"),
    path("create_alarm/", views.create_alarm, name="create_alarm"),
    path("delete_alarm/<int:alarm_id>/", views.delete_alarm, name="delete_alarm"),
    path("check_alarm/", views.check_alarm, name="check_alarm"),

]