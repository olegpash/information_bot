import random
import time
import datetime
import requests
import vk_api
from bs4 import BeautifulSoup


def get_world_stats(site_soup):
    title_phrase = site_soup.find('p', {'class': 'title_map'}).text.strip()
    middle_stats = site_soup.find('p', {'class': 'second'}).text.strip()
    world_and_russia_info = site_soup.find('div', {'class': 'top_new_block_information'})
    world_info = world_and_russia_info.find('div', {'class': 'stat_container'}).text.strip()
    world_statistic = '\nМировая статистика:\n' + world_info.replace('(', ' (').replace(')', ') ').replace('\n', ',\n')
    return title_phrase + '\n' + world_statistic + '.\n' + middle_stats.replace('в', 'заражений в') + '.\n\n'


def get_rf_stats(site_soup):
    middle_stats = site_soup.findAll('p', {'class': 'second'})[1].text.strip().replace('в', 'заражений в') + '.'

    world_and_russia_info = site_soup.find('div', {'class': 'top_new_block_information'})
    russia_info = world_and_russia_info.findAll('div', {'class': 'stat_container'})[1].text.strip().replace('(', ' (').replace(')', ') ')

    russia_statistic = 'Статистика распространения в России:\n' + russia_info.replace('\n', ',\n') + '.\n' + middle_stats
    return russia_statistic


def get_pnz_stats():

    site_url = 'https://koronavirus-today.ru/koronavirus-v-penzenskoj-oblasti-statistika-zabolevanij/'
    site_text = requests.get(site_url).text
    site_soup = BeautifulSoup(site_text, features="html.parser")
    pnz_find_res = site_soup.find('div', {'class': 'symptomi_page_content'}).text.strip().split('\n')[0:3]
    pnz_find_res[0], pnz_find_res[2] = pnz_find_res[0] + ':', pnz_find_res[2] + '.'
    return '\n\n' + '\n'.join(pnz_find_res)


def get_stats():
    site_url = 'https://koronavirus-today.ru/'
    site_text = requests.get(site_url).text
    site_soup = BeautifulSoup(site_text, features="html.parser")
    world_text = get_world_stats(site_soup)
    rf_text = get_rf_stats(site_soup)
    pnz_text = get_pnz_stats()
    result = world_text + rf_text + pnz_text
    return result


def error_report(vk, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': '218563368', 'message': message, 'random_id': random_id})

def send(vk, user_id, message):
    random_id = random.randint(1, 10000000)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def get_members(vk):
    answer = vk.method('groups.getMembers', {'group_id': '188989699'})
    return answer['items']


def start():
    token = "here is vk_token"
    vk = vk_api.VkApi(token=token)
    try:
        message_to_send = get_stats()
    except Exception:
        error_report(vk, 'Ошибка при получении данных о коронавирусе.')
        exit('Error receiving coronavirus data!')
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
    now = int(datetime.datetime.now().hour)
    if now == 13:
        start()
    time.sleep(3600)
