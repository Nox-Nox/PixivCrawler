import re
import time
from os import path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pickle


def new_login(driver):
    usernameField = '//*[@id="LoginComponent"]/form/div[1]/div[1]/input'
    passwordField = '//*[@id="LoginComponent"]/form/div[1]/div[2]/input'
    login_button = '//*[@id="LoginComponent"]/form/button'
    username = input("Enter your pixiv ID or E-mail ")
    password = input("Enter your password ")
    driver.get("https://accounts.pixiv.net/login")
    print(driver.title)
    # values inside send_keys will be replaced with the suername and password variables
    driver.find_element(By.XPATH, usernameField).send_keys(
        "nur.tahmid2022@gmail.com")
    driver.find_element(By.XPATH, passwordField).send_keys("DianaWgore99")
    driver.find_element(By.XPATH, login_button).click()
    time.sleep(2)
    print(driver.get_cookies())
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def saved_login(driver):
    print('logging in...')
    driver.get("https://pixiv.net")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://pixiv.net")


def display(list):
    for i in list:
        print(i)


def format_link_to_get_id(link):
    formatted = link.split('/', 3)[-1]
    return formatted


def format_link_to_download(original_link):
    start_formatted = re.sub('c/.*?250x250_80_a2/img-master',
                             'img-original', original_link, flags=re.DOTALL)
    full_formatted = re.sub(
        '_square1200', '', start_formatted, flags=re.DOTALL)
    return full_formatted


def get_arts_ids(response):
    ids = []
    for k, v in response.json().items():
        if k == 'body' and v['illusts']:
            for c, b in v['illusts'].items():
                ids.append(c)
    return ids


def choice(subject):
    choice = int()
    correct = True
    while correct:
        try:
            choice = int(input('which {}? '.format(subject)))
        except ValueError or IndexError:
            print("value is not a number or not between the given range, try again")
        else:
            correct = False

    return choice


def bulk_query_builder(ids):
    i = 1
    j = 1
    art_id_query = str()
    art_id_query_list = []
    if i < len(ids):
        for n in ids:
            if j < 50:
                art_id_query += 'ids%5B%5D={}&'.format(n)
                j += 1
                i += 1
            else:
                full_query_for_arts = 'https://www.pixiv.net/ajax/user/2188232/profile/illusts?' + \
                    art_id_query + 'work_category=illustManga&is_first_page=0&lang=en'
                art_id_query_list.append(full_query_for_arts)
                art_id_query = ''
                j = 1
                i += 1
        full_query_for_arts = 'https://www.pixiv.net/ajax/user/2188232/profile/illusts?' + \
            art_id_query + 'work_category=illustManga&is_first_page=0&lang=en'
        art_id_query_list.append(full_query_for_arts)
    return art_id_query_list


def get_artist_by_name(driver):
    artist_nick = input('enter artist name: ')
    driver.get(
        'https://www.pixiv.net/search_user.php?nick={}&s_mode=s_usr'.format(artist_nick))
    time.sleep(2)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    artist_results = []
    artists_selector = soup.findAll('li', class_='user-recommendation-item')
    i = 0
    for artist_selector in artists_selector:
        nick = artist_selector.find('a').get('title')
        link = artist_selector.find('a').get('href')
        id = format_link_to_get_id(link)
        artist = {i:
                  [
                      nick,
                      id,
                  ]
                  }
        artist_results.append(artist)
        i += 1
    return artist_results


def get_arts_of_chosen_artist(artist_results, choice):
    c = 'https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'.format(
        artist_results[choice][choice][1])
    response = requests.get(c)
    arts_id_list = get_arts_ids(response)
    art_id_query_list = bulk_query_builder(arts_id_list)
    illustrations = []
    i = 0
    for f in art_id_query_list:
        data = requests.get(f)
        for k, v in data.json()['body']['works'].items():
            art_id = v['id']
            title = v['title']
            url = format_link_to_download(v['url'])
            illustration = {
                i:
                [
                    art_id,
                    title,
                    url,
                ]
            }

            i += 1
            illustrations.append(illustration)
    return illustrations


if __name__ == "__main__":

    s = Service('chromedriver_linux64 (1)/chromedriver')
    o = Options()
    o.add_argument('--headless')
    driver = webdriver.Chrome(service=s, options=o)

    if path.exists("cookies.pkl"):
        saved_login(driver)
    else:
        new_login(driver)

    match = True
    while match:
        artist_results = get_artist_by_name(driver)
        print("search results:")
        if artist_results:
            display(artist_results)
            match = False
        else:
            print('no matches, search again')
            match = True

    correct = True
    while correct:
        picked_choice = choice('artist')
        if 0 <= picked_choice <= len(artist_results):
            print(artist_results[picked_choice][picked_choice][0],
                  ' ', artist_results[picked_choice][picked_choice][1])
            arts_of_chosen_artist = get_arts_of_chosen_artist(
                artist_results, picked_choice)
            display(arts_of_chosen_artist)
            picked_choice = choice('art')
            if 0 <= picked_choice <= len(arts_of_chosen_artist):
                print(arts_of_chosen_artist[picked_choice])
                driver.close()
            correct = False
        else:
            print("please choose a valid value between the given options: ")
