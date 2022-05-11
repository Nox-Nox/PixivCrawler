import time
import os.path
from os import path
from requests import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    driver.get("https://pixiv.net")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://pixiv.net")


def search_artist_by_name(driver):
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
        artist = {i:
                  [
                      nick,
                      'https://pixiv.net'+link+'/artworks?p=1',
                  ]
                  }
        artist_results.append(artist)
        i += 1
    return artist_results


def get_art_by_chosen_artist(driver, artist_results, choice):
    driver.get(artist_results[choice][choice][1])
    time.sleep(2)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    art_pages = soup.find(
        'nav', class_='sc-xhhh7v-0 kYtoqc')
    pages = len(art_pages.findAll('a'))-1

    art_results = []
    arts_selector = soup.findAll(
        'li', class_='sc-9y4be5-2 sc-9y4be5-3 sc-1wcj34s-1 kFAPOq CgxkO')

    i = 0
    title = str()

    for art_selector in arts_selector:
        artist_id = art_selector.find(
            'a', class_='sc-d98f2c-0 sc-rp5asc-16 iUsZyY sc-bdnxRM fGjAxR').get('data-gtm-user-id')
        link = art_selector.find(
            'a', class_='sc-d98f2c-0 sc-rp5asc-16 iUsZyY sc-bdnxRM fGjAxR').get('href')
        for a in art_selector.findAll('a')[1]:
            title = a.get_text()
            art = {i:
                   [
                       artist_id,
                       title,
                       'https://pixiv.net'+link,
                   ]
                   }
            art_results.append(art)
            i += 1
    return art_results


if __name__ == "__main__":

    s = Service('chromedriver_linux64 (1)/chromedriver')
    driver = webdriver.Chrome(service=s)

    if path.exists("cookies.pkl"):
        saved_login(driver)
    else:
        new_login(driver)

    match = True
    while match:
        artist_results = search_artist_by_name(driver)
        print("search results:")
        if artist_results:
            for c in artist_results:
                print(c)
            match = False
        else:
            print('no matches, search again')
            match = True

    correct = True
    while correct:
        try:
            choice = int(input('which artist? '))
        except ValueError or IndexError:
            print("value is not a number or not between the given range, try again")
        if 0 <= choice <= len(artist_results):
            print(artist_results[choice][choice][0])
            print(artist_results[choice][choice][1])
            get_art_by_chosen_artist(driver, artist_results, choice)
            correct = False
        else:
            print("please choose a valid value between the given options: ")
