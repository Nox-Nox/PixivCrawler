import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


username = '//*[@id="LoginComponent"]/form/div[1]/div[1]/input'
password = '//*[@id="LoginComponent"]/form/div[1]/div[2]/input'
login_button = '//*[@id="LoginComponent"]/form/button'
search_bar = '//*[@id="root"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/form/div/input'
search_mode_user_click = '//*[@id="root"]/div[2]/div[2]/div/div[5]/nav/a[5]'

search_user = 'https://www.pixiv.net/search_user.php?nick={artist_nick}&s_mode=s_usr'
artist_nick = str()


s = Service('chromedriver_linux64 (1)/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get("https://accounts.pixiv.net/login")
print(driver.title)


driver.find_element(By.XPATH, username).send_keys(
    "nur.tahmid2022@gmail.com")
driver.find_element(By.XPATH, password).send_keys("DianaWgore99")
driver.find_element(By.XPATH, login_button).click()
time.sleep(2)

artist_nick = input('enter artist name: ')
# driver.find_element_by_xpath(search_bar).send_keys(artist, Keys.ENTER)
# driver.find_element(By.NAME, search_mode_user_click).click()
page = driver.get(
    'https://www.pixiv.net/search_user.php?nick={}&s_mode=s_usr'.format(artist_nick))

time.sleep(4)
source = driver.page_source
soup = BeautifulSoup(source, 'lxml')
# print(soup.prettify())
artist_results = []
artists_selector = soup.findAll('li', class_='user-recommendation-item')
for artist_selector in artists_selector:
    i = 0
    nick = artist_selector.find('a').get('title')
    link = artist_selector.find('a').get('href')
    artist = {
        'id': i,
        'artist': nick,
        'link': 'pixiv.net'+link,
    }
    artist_results.append(artist)
    i += 1

for c in artist_results:
    print("search results: ", c)

choice = input('which artist? ')
# try:
#     WebDriverWait(driver, 40).until(
#         EC.presence_of_element_located(
#             (By.XPATH, search_mode_user_click))  # This is a dummy element
#     )
# finally:
#     driver.find_element(By.XPATH, search_mode_user_click).click()

# user_recomm = driver.find_element(
#     By.XPATH, '//*[@id="wrapper"]/div[1]/div/div[3]/ul')

# users = user_recomm.find_elements(By.TAG_NAME, 'h1')

# for user in users:
#     print(user.text)
