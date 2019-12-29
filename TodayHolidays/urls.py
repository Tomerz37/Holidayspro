from django.urls import path
from TodayHolidays import views

app_name = 'TodayHolidays'

urlpatterns = [
    # /TodayHolidays/
    path('', views.index, name='index'),


]
