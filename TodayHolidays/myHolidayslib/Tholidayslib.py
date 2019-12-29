import sqlite3
import traceback
import requests
import json
import calendar
import pendulum
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#  connect to DB
connection = sqlite3.connect('GHolidays.db', check_same_thread=False)
c = connection.cursor()
connection.execute('''CREATE TABLE IF NOT EXISTS Holiday(
                    "date"	TEXT NOT NULL,
                    "name"	TEXT NOT NULL,
                    "country"	TEXT NOT NULL)''')
class Check_holiday:
    is_holiday = False

    def makeTrue(self):
        is_holiday = True
        return ''

    def makeFalse(self):
        is_holiday = False
        return ''

class Holiday:

    def __init__(self, date, name, country):
        self.date = str(date)
        self.name = str(name)
        self.country = str(country)

    def __str__(self):
        return {'date': self.date, 'name': self.name, 'country': self.country}

    def holidaydate(self):
        return self.date

    def holidayName(self):
        return self.name

    def holidayCountry(self):
        return self.country

# list of countries for API use
def getallCountriesforAPI():
    all_countries = [{'region': 'US', 'country': 'United states'},
                     {'region': 'JP', 'country': 'Japan'},
                     {'region': 'CA', 'country': 'Canada'},
                     {'region': 'DE', 'country': 'Germany'},
                     {'region': 'ZW', 'country': 'Zimbabwe'},
                     {'region': 'ES', 'country': 'Spain'},
                     {'region': 'NL', 'country': 'Netherlands'},
                     {'region': 'CH', 'country': 'Switzerland'},
                     {'region': 'GB', 'country': 'United Kingdom'},
                     {'region': 'SE', 'country': 'Sweden'},
                     {'region': 'ZA', 'country': 'South Africa'},
                     {'region': 'SG', 'country': 'Singapore'},
                     {'region': 'FR', 'country': 'France'},
                     {'region': 'AU', 'country': 'Australia'},
                     {'region': 'BW', 'country': 'Botswana'},
                     {'region': 'CZ', 'country': 'Czechia'},
                     {'region': 'EC', 'country': 'Ecuador'},
                     {'region': 'MX', 'country': 'Mexico'},
                     {'region': 'PL', 'country': 'Poland'},
                     {'region': 'TR', 'country': 'Turkey'},
                     {'region': 'VN', 'country': 'Vietnam'}
                     ]
    return all_countries

# list of countries for DB use
def getallcountriesforDB():
    all_countries = {'US': 'United states',
                      'JP': 'Japan',
                      'CA': 'Canada',
                      'DE': 'Germany',
                      'ZW': 'Zimbabwe',
                      'ES': 'Spain',
                      'NL': 'Netherlands',
                      'CH': 'Switzerland',
                      'GB': 'United Kingdom',
                      'SE': 'Sweden',
                      'ZA': 'South Africa',
                      'SG': 'Singapore',
                      'FR': 'France',
                      'AU': 'Australia',
                      'BW': 'Botswana',
                      'CZ': 'Czechia',
                      'EC': 'Ecuador',
                      'MX': 'Mexico',
                      'PL': 'Poland',
                      'TR': 'Turkey',
                      'VN': 'Vietnam',
                      }
    return all_countries

#get local time and change it's pattern to fit the api pattern
def get_local_time():
    today_date = pendulum.now()
    today_date_str = ""
    if today_date.day < 10:
        today_date_str = str(today_date.year) + '-' + str(today_date.month) + '-' + '0' + str(today_date.day)
    else:
        today_date_str = str(today_date.year) + '-' + str(today_date.month) + '-' + str(today_date.day)

    if today_date.month < 10:
        if today_date.day < 10:
            today_date_str = str(today_date.year) + '-' + '0' + str(today_date.month) + '-' + '0' + str(
                today_date.day)
        else:
            today_date_str = str(today_date.year) + '-' + '0' + str(today_date.month) + '-' + str(today_date.day)
    else:
        if today_date.day < 10:
            today_date_str = str(today_date.year) + '-' + str(today_date.month) + '-' + '0' + str(today_date.day)
        else:
            today_date_str = str(today_date.year) + '-' + str(today_date.month) + '-' + str(today_date.day)
    return today_date_str

# get all the data from api
def create_all_holidays():
    all_countries = getallCountriesforAPI()
    all_holidays = []
    today_date = pendulum.now()
    headers = {
        'x-rapidapi-host': "public-holiday.p.rapidapi.com",
        'x-rapidapi-key': "2bbcb4b15cmsha362b48399c468ep155048jsn8b630311434a"
    }
    for country in range(0, len(all_countries)):
        url = f"https://public-holiday.p.rapidapi.com/{today_date.year}/{all_countries[country]['region']}"
        response = requests.request("GET", url, headers=headers)
        try:
            all_holidays.append(json.loads(response.text))
        except:
            pass
    return all_holidays

# insert holidays to DB
def insertHoliday(date, name, country):
    try:
        connection.execute("INSERT INTO Holiday VALUES (?,?,?)",
                           (date, name, country))
        connection.commit()

    except:
        traceback.print_exc()
        print('Error in inserting Holiday')

# updated DB from api with the help of create_all_holidays() & insertHoliday()
def update_holidays_DB():  # use once a year!
    a = create_all_holidays()
    all_countries = getallcountriesforDB()
    for h1 in a:
        for h2 in h1:
            try:
                if (not check_if_holiday_in_DB(h2['date'], h2['name'], all_countries[h2['countryCode']])):
                    insertHoliday(h2['date'], h2['name'], all_countries[h2['countryCode']])
            except KeyError:
                print("KeyError", KeyError)
    print('DONE')

#  get all holidays from DB
def getAllHolidays():
    try:
        c.execute("SELECT * FROM Holiday")
        return c.fetchall()
    except:
        print('Error in select all')
        traceback.print_exc()
        return -1
# print(getAllHolidays())
#  get all the holidays that occurs on a specific date from DB
def getHolidayPerDate(date):
    try:
        c.execute("SELECT * FROM Holiday WHERE date = {}".format("'" + date + "'"))
        return c.fetchall()
    except:
        print('Error in HolidayPerDate')
        traceback.print_exc()
        return -1

#  check if there are holidays on a specific date (boolian func)
def isHoliday(date):
    try:
        c.execute("SELECT * FROM Holiday WHERE date = {}".format("'" + date + "'"))
        if len(c.fetchall()) > 0:
            return True
        else:
            return False
    except:
        print('Error in isHoliday')
        traceback.print_exc()

# function to prevent duplicates on DB
def check_if_holiday_in_DB(date, name, country):
    c.execute("SELECT * FROM Holiday WHERE date = ? AND name = ? AND country = ?", (date, name, country))
    if len(c.fetchall()) > 0:
        return True
    else:
        return False

#  update_holidays_DB()

'''
def get_today_holidays():
    all_holidays = create_all_holidays()
    today_holidays = []
    today_date = get_local_time()
    for h1 in range(0, len(all_holidays)):
        for h2 in range(0, len(all_holidays[h1])):
            if all_holidays[h1][h2]['date'] == today_date:
                today_holidays.append(all_holidays[h1][h2])
    return today_holidays
''' #get today holidays
'''
def get_holidays_per_date(date):
    all_holidays = create_all_holidays()
    this_week_holidays = []
    for h1 in range(0, len(all_holidays)):
        for h2 in range(0, len(all_holidays[h1])):
            if all_holidays[h1][h2]['date'] == date:
                this_week_holidays.append(all_holidays[h1][h2])
    return this_week_holidays
''' #get holidays per date
'''
def get_this_week_dates():
    this_week = []
    for count in range(0, 7):
        this_week.append((calendar.day_name[calendar.weekday(pendulum.now().add(days=count).year,
                                                             pendulum.now().add(days=count).month,
                                                             pendulum.now().add(days=count).day)],
                          pendulum.now().add(days=count).date()))
    return this_week
''' #get this week dates
'''
def get_this_week_holidays():
    this_week_holidays_list = []
    week_dates = get_this_week_dates()
    for d in week_dates:
        this_week_holidays_list.append(getHolidayPerDate(str(d[1])))
        if len(d) != 0:
            this_week_holidays_list.append('No Holidays Today')
    return this_week_holidays_list
''' #get this week holidays


