import requests
import json
import datetime as dt
import random


def get_vacancies():
    all_vacancies = main()
    data = []
    nums = []
    while len(nums) < 3:
        n = random.randint(1, len(all_vacancies)+1)
        if n not in nums:
            nums.append(n)
    for i in nums:
        data.append(all_vacancies[i])
    return data

def get_salary_vacancies():
    all_vacancies = main()
    data = []
    nums = []
    while len(nums) < 3:
        n = random.randint(1, len(all_vacancies))
        if (all_vacancies[n]['Заработная плата']['От'] != 'Не указана'
                and all_vacancies[n]['Заработная плата']['До'] != 'Не указана'
                and (n not in nums)):
            nums.append(n)
    for i in nums:
        data.append(all_vacancies[i])
    return data

def get_vacancies_pages(url: str):
    area = 2
    per_page = 100
    text = 'python'

    params = {
        'area': area,
        'per_page': per_page,
        'text': text
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    return data['pages'], data['found']

def get_data_page(url: str, page: int):
    params = {
        'area': 2,
        'per_page': 100,
        'page': page,
        'text': 'python'
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    return data

def parse_page(data: dict) -> dict:
    vacancies = {}
    items = data['items']
    n = 1
    for i in items:
        id_1 = n
        vacancies[id_1] = {}
        vacancies[id_1]['Название'] = i['name']
        if i.get('address'):
            if i['address'].get('raw'):
                address = i['address']['raw']
                vacancies[id_1]['Адрес'] = address
            if i['address'].get('metro') and i['address']['metro'].get('station_name'):
                metro = i['address']['metro']['station_name']
                vacancies[id_1]['Станция метро'] = metro
        date = dt.datetime.strptime(i['published_at'][0:10], '%Y-%m-%d').date().strftime('%d.%m.%Y')
        #Тут можно было бы и срезом обойтись, но мне хотелось, чтобы дата смотрелась привычнее
        vacancies[id_1]['Дата публикации'] = date
        url = i['alternate_url']
        vacancies[id_1]['url'] = url
        if i.get('snippet') and i['snippet'].get('requirement'):
            snippet = i['snippet']['requirement']
            vacancies[id_1]['Требования'] = snippet
        if i.get('salary'):
            vacancies[id_1]['Заработная плата'] = {}
            currency = i['salary']['currency']
            if i['salary'].get('from'):
                fro = i['salary']['from']
                vacancies[id_1]['Заработная плата']['От'] = fro
                vacancies[id_1]['Заработная плата']['Валюта от'] = currency
            else:
                vacancies[id_1]['Заработная плата']['От'] = 'Не указана'
                vacancies[id_1]['Заработная плата']['Валюта от'] = ''
            if i['salary'].get('to'):
                t = i['salary']['to']
                vacancies[id_1]['Заработная плата']['До'] = t
                vacancies[id_1]['Заработная плата']['Валюта до'] = currency
            else:
                vacancies[id_1]['Заработная плата']['До'] = 'Не указана'
                vacancies[id_1]['Заработная плата']['Валюта до'] = ''
        else:
            vacancies[id_1]['Заработная плата'] = {}
            vacancies[id_1]['Заработная плата']['От'] = 'Не указана'
            vacancies[id_1]['Заработная плата']['До'] = 'Не указана'
            vacancies[id_1]['Заработная плата']['Валюта от'] = ''
            vacancies[id_1]['Заработная плата']['Валюта до'] = ''
        if i.get('experience') and i['experience'].get('name'):
            experience = i['experience']['name']
            vacancies[id_1]['Требуемый опыт'] = experience
        n += 1
    return vacancies

def main():
    vacancies = {}
    url_api = 'https://api.hh.ru/vacancies'
    pages, found  = get_vacancies_pages(url=url_api)
    for i in range(1, pages):
        data_page = get_data_page(url=url_api, page=i)
        page = parse_page(data_page)
        vacancies = {**vacancies, **page}
    return vacancies