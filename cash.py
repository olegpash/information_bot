import ast
import random
import time
import requests
import vk_api
from bs4 import BeautifulSoup


def converter(data):
    a = '1234567890.,'
    st = ''
    for i in range(len(data)):
        if str(data[i]) in a:
           st += str(data[i])
    return st
def main():
    dollar = 'https://www.google.com/search?sxsrf=ALeKk01PJCR_1wfskarIN5hk_Yyilri0xg%3A1591964268098&ei=bHLjXoTBBcusrgTh14bwCQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgUIABCxAzIFCAAQsQMyAggAMgUIABCxAzIFCAAQsQMyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDOgQIIxAnOgcIABCxAxBDOgQIABBDOgoIABCxAxAUEIcCUIcdWIAvYOYvaABwAHgAgAFZiAGGB5IBAjEymAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiEp8eFofzpAhVLlosKHeGrAZ4Q4dUDCAw&uact=5'
    euro = 'https://www.google.com/search?sxsrf=ALeKk012L2q0DYFJEkBAlSIfc8-21HJgtA%3A1585516200432&ei=qA6BXpX7GZuWjgbYsYbYCg&q=%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgQIABBDMgUIABCDATICCAAyBAgAEEMyAggAMgIIADIECAAQQzIECAAQQzICCAA6BAgAEEc6BwgjELACECc6BAgAEA06BAgjECc6CggAEIMBEBQQhwI6BwgjEOoCECc6BggAEAoQAToICAAQChABECpQkMAgWLvdIGDk3yBoBHABeAKAAbgBiAGGCZIBBDEzLjGYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab&ved=0ahUKEwiV76WPzMDoAhUbi8MKHdiYAasQ4dUDCAs&uact=5'
    funt = 'https://www.google.com/search?sxsrf=ALeKk00ecHAwnkwcx9pk-AlHykX7Eqhljg%3A1585516737912&ei=wRCBXu-oN-2cmwX3l6q4AQ&q=%D1%84%D1%83%D0%BD%D1%82&oq=%D1%84%D1%83%D0%BD%D1%82&gs_lcp=CgZwc3ktYWIQAzIECCMQJzIECCMQJzIECCMQJzIECAAQQzIECAAQQzIECAAQQzIFCAAQgwEyBAgAEEMyAggAMgQIABBDOgQIABBHUJSMAljLlAJgppYCaABwAXgAgAFViAGoApIBATSYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwivjcuPzsDoAhVtzqYKHfeLChcQ4dUDCAs&uact=5'
    btc = 'https://www.google.com/search?q=btc+usd&oq=btc&aqs=chrome.1.69i57j0l7.2830j0j7&sourceid=chrome&ie=UTF-8'
    sp = [dollar, euro, funt, btc]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}
    count = 0
    d = {}
    for valuta in sp:
        count += 1
        try:
            full_page = requests.get(valuta, headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert = soup.find_all('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
            if count == 1:
                d['usd'] = converter(convert[0].text)
            if count == 2:
                d['euro'] = converter(convert[0].text)
            if count == 3:
                d['funt'] = converter(convert[0].text)
            if count == 4:
                d['btc'] = converter(convert[0].text)
                break
        except Exception:
            pass
    if 'usd' not in d.keys():
        d['usd'] = 0
    if 'euro' not in d.keys():
        d['euro'] = 0
    if 'funt' not in d.keys():
        d['funt'] = 0
    if 'btc' not in d.keys():
        d['btc'] = 0
    return d


def write_to_txt(data):
    with open('cash_data.txt', 'w', encoding='utf-8') as log:
        log.write(str(data))


def get_from_txt():
    return ast.literal_eval(open(r'cash_data.txt', "r", encoding='UTF-8').read().split('\n')[0])


def delta(now, start):
    usd_d = str(round(float(str(now['usd']).replace(',', '.')) - float(str(start['usd']).replace(',', '.')), 2)).replace('.', ',')
    if usd_d[0] != '-':
        usd_d = '+' + usd_d + '₽'

    euro_d = str(round(float(str(now['euro']).replace(',', '.')) - float(str(start['euro']).replace(',', '.')), 2)).replace('.', ',')
    if euro_d[0] != '-':
        euro_d = '+' + euro_d + '₽'

    funt_d = str(round(float(str(now['funt']).replace(',', '.')) - float(str(start['funt']).replace(',', '.')), 2)).replace('.', ',')
    if funt_d[0] != '-':
        funt_d = '+' + funt_d + '₽'

    btc_d = str(round(float(str(now['btc']).replace(',', '.')) - float(str(start['btc']).replace(',', '.')), 2)).replace('.', ',')
    if btc_d[0] != '-':
        btc_d = '+' + btc_d + '$'

    return {'usd': usd_d, 'euro': euro_d, 'funt': funt_d, 'btc': btc_d}

def error_report(vk, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': '218563368', 'message': message, 'random_id': random_id})

def send(vk, user_id, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def get_members(vk):
    answer = vk.method('groups.getMembers', {'group_id': '188989699'})
    return answer['items']


def start(rezhim):
    token = "vk token"
    vk = vk_api.VkApi(token=token)
    try:
        data = main()  # now
        if rezhim == 'start':
            write_to_txt(data)
            res = f'Данные по валютам на текущее время\nДоллар: {data["usd"]}₽,\nЕвро: {data["euro"]}₽,\nФунт: {data["euro"]}₽,\nБиткоин: {data["btc"]}$.'
        elif rezhim == 'stop':
            data_2 = get_from_txt()  # start
            data_3 = delta(data, data_2)  # delta
            res = f'Данные по валютам на текущее время\nДоллар: {data["usd"]}₽ ({data_3["usd"]} за день),' \
                     f'\nЕвро: {data["euro"]}₽ ({data_3["euro"]} за день),\nФунт: {data["funt"]}₽ ({data_3["funt"]}' \
                     f' за день),\nБиткоин: {data["btc"]}$ ({data_3["btc"]}$ за день).'
    except Exception:
        error_report(vk, 'Ошибка при получении данных о cashe.')
        exit('Getting cash error!')

    try:
        members_list = get_members(vk)
    except Exception:
        error_report(vk, 'Ошибка при получении подписчиков сообщества!')
        exit('Error getting community subscribers!')
    for i in members_list:
        try:
            send(vk, i, res)
        except Exception:
            pass


while True:
    start('start')
    time.sleep(60*60*12)
    start('stop')
    time.sleep(60*60*12)

