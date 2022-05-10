import time
import os.path
from os import path
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
    driver.find_element(By.XPATH, usernameField).send_keys(
        "nur.tahmid2022@gmail.com")
    driver.find_element(By.XPATH, passwordField).send_keys("DianaWgore99")
    driver.find_element(By.XPATH, login_button).click()
    time.sleep(2)
    print(driver.get_cookies())
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def saved_login(driver):
    driver.get("https://pixiv.net")
    time.sleep(1)
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://pixiv.net")


def searchArtist(driver):
    artist_nick = input('enter artist name: ')
    driver.get(
        'https://www.pixiv.net/search_user.php?nick={}&s_mode=s_usr'.format(artist_nick))
    time.sleep(4)
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
                      'pixiv.net'+link,
                  ]
                  }
        artist_results.append(artist)
        i += 1
    return artist_results


if __name__ == "__main__":

    s = Service('chromedriver_linux64 (1)/chromedriver')
    driver = webdriver.Chrome(service=s)

    if path.exists("cookies.pkl"):
        saved_login(driver)
    else:
        new_login(driver)

    match = True

    artist_results = searchArtist(driver)
    while match:
        print("search results:")
        if artist_results:
            for c in artist_results:
                print(c)
            match = False
        else:
            print('no matches, search again')
            match = True
            searchArtist()

    choice = int(input('which artist? '))

    if isinstance(choice, int) and 0 <= choice <= len(artist_results):
        print(artist_results[choice])
