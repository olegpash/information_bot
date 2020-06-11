import random

import vk_api
from bs4 import BeautifulSoup
import requests
import time


def send(vk, user_id, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def get_members(vk):
    answer = vk.method('groups.getMembers', {'group_id': '188989699'})
    return answer['items']


def error_report(vk, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': '218563368', 'message': message, 'random_id': random_id})


def get_data():
    url_weather = 'https://yandex.ru/pogoda/penza'
    url_date = 'http://www.xn--80aajbde2dgyi4m.xn--p1ai/'
    url_date_2 = 'https://bbf.ru/calendar/today/'
    date_text = requests.get(url_date).text
    date_soup = BeautifulSoup(date_text, features="html.parser")
    phrase = date_soup.find('p', {'id': 'dayparts'}).text.strip()
    date_text = requests.get(url_date_2).text
    date_soup = BeautifulSoup(date_text, features="html.parser")
    now_date = date_soup.findAll('div', {'class': 'calendar__title'})[1].text + '.'.strip()
    text = requests.get(url_weather).text
    soup = BeautifulSoup(text, features="html.parser")
    now_temperature = soup.find('span', {'class': 'temp__value'}).text.strip()
    now_time = soup.find('time', {'class': 'time fact__time'}).text.strip()
    yesterday_temperature = soup.find('div', {'class': 'term term_orient_h fact__yesterday'}).text.strip()[17::]
    weather_status = soup.find('div', {'class': 'link__condition day-anchor i-bem'}).text.strip()
    feeling_weather = soup.find('div', {'class': 'fact__hour-temp'}).text.strip()  # ощущается как
    return str(str(phrase) + '\n' + str(now_date) + '\n' + str(now_time) + '\nТемпература ' + str(now_temperature)
               + '°C.\nОщущается как ' + str(feeling_weather) + 'C.\nВчера в это время было ' +
               str(yesterday_temperature) + 'C.\nНа улице сейчас ' + str(weather_status).lower() + '.')


def start():
    token = "тут секретный токен вк"
    vk = vk_api.VkApi(token=token)
    try:
        message_to_send = get_data()
    except Exception:
        error_report(vk, 'Ошибка при получении данных о погоде.')
        exit('Error while receiving weather data!')
    try:
        members_list = get_members(vk)
    except Exception:
        error_report(vk, 'Ошибка при получении подписчиков сообщества!')
        exit('Error getting community subscribers!')
    for i in members_list:
        try:
            send(vk, i, message_to_send)
        except Exception:
            pass


while True:
    start()
    time.sleep(14400)
