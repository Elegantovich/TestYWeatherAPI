import datetime

import pandas as pd
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .models import Report
from .serializers import ReportSerializer

PRESSURE_UP = 'Ожидается резкое увеличение атмосферного давления'
PRESSURE_DOWN = 'Ожидается резкое падение атмосферного давления'
HEAD = ('Время суток', 'Температура', 'Погодное явление',
        'Давление, мм', 'Влажность')
content_type = ('application/vnd.openxmlformats-'
                'officedocument.spreadsheetml.sheet')


def to_excel(week, day):
    """Send data to ecxel document."""
    data = []
    for item in week:
        data += item
    data_table = pd.DataFrame(data, columns=HEAD)
    data_table.to_excel('WeekWeather.xlsx',
                        sheet_name=f'{str(day-7)}-{str(day)}',
                        index=False)
    return data_table


def create_report(city, error_exist):
    """Work with DB."""
    report = {'city': city,
              'result': error_exist}
    ReportSerializer(report)
    Report.objects.create(city=city, result=error_exist)


class ReportView(APIView):
    def post(self, request):
        city = request.data.get('city')
        count, count2, count3 = 0, 0, 0
        date = datetime.datetime.today().strftime('.%m.%Y')
        count, count2, count3 = 0, 0, 0
        weather_list, day_list, mid_time, = [], [], []
        week, pressure_list, mid_val_list = [], [], []
        day = int(datetime.datetime.today().strftime('%d'))
        try:
            d = webdriver.Chrome('chromedriver.exe')
            d.get(f'https://yandex.ru/pogoda/{city}/details?via=ms#{day}')
            WebDriverWait(d, 10)
            body = d.find_elements(By.XPATH,
                                   "//*[@class='forecast-fields']")
            mag_list = [' '.join(i.text.split()[3:]) for i in body]
            if len(mag_list) == 0:
                raise Exception('Error, check the input data!')
            body = d.find_elements(By.XPATH,
                                   "//*[@class='weather-table']/tbody/tr/td")
            for item in body:
                if count == 2:
                    weather_list += [' '.join(item.text.split())]
                else:
                    if count < 5:
                        weather_list += item.text.split()
                if count == 3:
                    pressure_list.append(int(item.text))
                    if len(pressure_list) == 4:
                        morning_pressure = pressure_list[0]
                        for pressure in pressure_list[1:]:
                            if abs(morning_pressure - pressure) >= 5:
                                if pressure > morning_pressure:
                                    str_pressure = PRESSURE_UP
                                    break
                                else:
                                    str_pressure = PRESSURE_DOWN
                                    break
                            str_pressure = None
                        pressure_list = []
                count += 1
                if count == 7:
                    day_list.append(weather_list)
                    weather_list = []
                    count = 0
                if len(day_list) == 4:
                    for time in day_list:
                        mid_time = mid_time + time[1].split('…')
                        if count3 == 2:
                            m_tuple = tuple(map(int, mid_time))
                            mid_val = round((sum(m_tuple) / len(m_tuple)), 1)
                            mid_val_list.append(mid_val)
                            mid_time = []
                            count3 = 0
                            break
                        count3 += 1
                    try:
                        day_list.append([f'{day}{date}',
                                        'Средняя дневная t = '
                                         f'{mid_val_list[count2]}',
                                         str_pressure, mag_list[count2], ''])
                    except IndexError:
                        day_list.append([f'{day}{date}',
                                        'Средняя дневная t = '
                                         f'{mid_val_list[count2]}',
                                         str_pressure, None, ''])
                    week.append(day_list)
                    day_list = []
                    day += 1
                    count2 += 1
                if len(week) == 7:
                    break
            table = to_excel(week, day)
        except Exception as error:
            error_exist = str(error)
            return Response({"Error": error_exist},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            error_exist = 'Successful'
            filename = 'WeekWeather.xlsx'
            resp = HttpResponse(table, content_type=content_type)
            resp['Content-Disposition'] = f'attachment; filename={filename}'
            return resp
        finally:
            create_report(city, error_exist)
            d.close()
