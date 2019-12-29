from django.shortcuts import render
import myHolidayslib
import pendulum


def index(request):
    today_date = myHolidayslib.get_local_time()
    if_holiday = myHolidayslib.isHoliday(today_date)
    today_holiday = myHolidayslib.getHolidayPerDate(today_date)
    return render(request, 'TodayHolidays/index.html',
                  {'all_holidays': myHolidayslib.getAllHolidays(), 'today_date': today_date, 'if_holiday': if_holiday,
                   'all_countries': myHolidayslib.getallCountriesforAPI, 'today_holiday': today_holiday})


