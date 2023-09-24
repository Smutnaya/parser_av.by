import math

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from Cars import Cars

# driver = webdriver.Firefox()
# time.sleep(2)
models = {}
cars = []
driver = webdriver
count_items = 0


# проверяем данные url
def get_url(url):
    if url:
        return url
    else:
        raise 'url не найден'


# разворачивает список всех доступных авто
def get_all_auto(url, driver):
    driver.get(url)
    element = driver.find_element(By.CLASS_NAME, 'catalog--rich').find_element(By.CLASS_NAME, 'catalog__show-all')
    element = element.find_element(By.TAG_NAME, 'button')
    element.click()


def input_model():
    print('\n\nДля продолжения поиска введите одну из доступных моделей')

    model = 'x7'
    print(f'->model->{model}')
    # !!!
    # model = input('-> ').lower().strip()
    if model:
        return model
    else:
        raise 'Данные не найдены'


# выводим список доступных моделей заданного авто
def models_add(sections_link):
    print('Доступны следующие модели:')
    for s in sections_link:
        auto_title = str(s.get('title')).strip().lower()
        print(auto_title, end='   ')
        models.update({auto_title: s.get('href')})


# выполняем поиск ссылки на авто BMW и переходим по ней
def get_auto(url, driver):
    driver.get(url)
    auto = driver.find_element(By.CSS_SELECTOR, '[title*="BMW"]')
    # url = driver.current_url
    # print(url)
    url = get_url(str(auto.get_attribute('href')))
    auto.click()
    return url


# получаем модели автомобилей
def get_model_auto(url):
    url = get_url(url)
    page = requests.get(url)

    if page.status_code == 200:  # page.status_code - статус код '200'- успешно подключены, всё ок
        soup = BeautifulSoup(page.text, "html.parser")
        sections_link = soup.findAll('a', class_='catalog__link')

        if sections_link:
            models_add(sections_link)
        else:
            raise 'Авто указанной модели не найдены'


def model_auto(url_av, url, url_auto, driver):
    url = get_url(url)
    driver.get(url)
    href = f'[href="{url_auto}"]'
    driver.find_element(By.CSS_SELECTOR, href).click()
    url = url_av + url_auto
    return url


def get_count_items(url):
    url = get_url(url)
    page = requests.get(url)
    if page.status_code == 200:  # page.status_code - статус код '200'- успешно подключены, всё ок
        soup = BeautifulSoup(page.text, "html.parser")
        count_ = soup.find('h3', class_='listing__title').text.split(' ')[1]
        return int(count_)


# def next_str(url):
#     url = get_url(url)
#     page = requests.get(url)
#     if page.status_code == 200:  # page.status_code - статус код '200'- успешно подключены, всё ок
#         soup = BeautifulSoup(page.text, "html.parser")
#         url_data = soup.find('div', class_='paging__button')
#         soup = BeautifulSoup(str(url_data), "html.parser")
#         url = soup.find('a', class_='button button--default')
#         print(url)
#         return 'https://cars.av.by' + url.get('href')


def pars_top(soup):
    # listing-top__summary
    data_pars = soup.findAll('div', class_='listing-top__summary')
    soup = BeautifulSoup(str(data_pars), "html.parser")
    # model, url, byn, usd, data
    model = soup.findAll('span', class_='link-text')
    url = soup.findAll('a', class_='listing-top__title-link')
    price_html = soup.findAll('div', class_='listing-top__price-byn')
    soup_price = BeautifulSoup(str(price_html), "html.parser")
    byn = soup_price.findAll('span')
    usd = soup.findAll('div', class_='listing-top__price-usd')
    data = soup.findAll('div', class_='listing-top__params')
    for x in range(len(data_pars)):
        car = Cars(model[x].text, 'https://cars.av.by' + url[x].get('href'),
                   int(byn[x].text.replace('\xa0', '').replace('\u2009', '')),
                   int(str(usd[x].text)[2:-2].replace('\xa0', '').replace('\u2009', '')), data[x].text)
        cars.append(car)
        # print(car.model)


def pars_auto(url, page_auto):
    url = get_url(url)
    page = requests.get(url)
    if page.status_code == 200:  # page.status_code - статус код '200'- успешно подключены, всё ок
        soup = BeautifulSoup(page.text, "html.parser")

        if page_auto == 1:
            pars_top(soup)
            page_auto += 1
        # listing - item__wrap
        soup = BeautifulSoup(page.text, "html.parser")
        data_pars = soup.findAll('div', class_='listing-item')
        soup = BeautifulSoup(str(data_pars), "html.parser")
        model_pars = soup.findAll('h3', class_='listing-item__title')
        model_soup = BeautifulSoup(str(model_pars), "html.parser")
        model = model_soup.findAll('span', class_='link-text')
        url = model_soup.findAll('a', class_='listing-item__link')
        byn = soup.findAll('div', class_='listing-item__price')
        usd = soup.findAll('div', class_='listing-item__priceusd')
        data = soup.findAll('div', class_='listing-item__params')
        for x in range(len(data_pars)):
            car = Cars(model[x].text, 'https://cars.av.by' + url[x].get('href'),
                       int(byn[x].text.replace('\xa0', '').replace('\u2009', '').replace('р.', '')),
                       int(str(usd[x].text)[2:-2].replace('\xa0', '').replace('\u2009', '')), data[x].text)
            cars.append(car)


def parsing(url, driver):
    webdriver = driver
    url_av_by = url
    get_all_auto(url_av_by, webdriver)
    url_av = get_auto(url_av_by, webdriver)
    get_model_auto(url_av)
    model_inp = input_model()
    url_model = models[model_inp]
    url_av = model_auto(url_av_by, url_av, url_model, webdriver)
    count_items = math.ceil(get_count_items(url_av) / 25)
    page_auto = 1
    pars_auto(url_av, page_auto)
    while True:
        page_auto += 1
        if page_auto <= count_items:
            # print(page_auto, count_items)
            next_url = (
                    'https://cars.av.by/filter?brands%5B0%5D%5Bbrand%5D=8&brands%5B0%5D%5Bmodel%5D=5965&price_currency=2&page='
                    + str(page_auto))
            # next_url = next_str(url)
            # # print(next_url)
            # if next_url:
            pars_auto(next_url, page_auto)
        else:
            break

    print(f'\nВсего найдено объявлений: {len(cars)}\n')
    cars.sort(key=lambda x: x.usd, reverse=True)
    for car in cars:
        print(car.__str__())

# link = driver.current_url
# print(link)
