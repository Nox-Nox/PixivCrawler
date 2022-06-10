from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import requests
import pickle
import time
import re


def new_login(driver):
    usernameField = 'form.sc-y2pfnd-2.cLXqZh  fieldset.sc-bn9ph6-0.kJkgq.sc-y2pfnd-5.hwSAwj label.sc-bn9ph6-1.hJBrSP input.sc-bn9ph6-6.degQSE'
    passwordField = 'form.sc-y2pfnd-2.cLXqZh  fieldset.sc-bn9ph6-0.kJkgq.sc-y2pfnd-6.ioPdtV label.sc-bn9ph6-1.hJBrSP input.sc-bn9ph6-6.hfoSmp'
    login_button = 'form.sc-y2pfnd-2.cLXqZh button.sc-bdnxRM.jvCTkj.sc-dlnjwi.pKCsX.sc-y2pfnd-9.dMhwJU.sc-y2pfnd-9.dMhwJU'
    username = input("Enter your pixiv ID or E-mail: ")
    password = input("Enter your password: ")
    driver.get("https://accounts.pixiv.net/login")
    driver.find_element(By.CSS_SELECTOR, usernameField).send_keys(
        username)
    driver.find_element(By.CSS_SELECTOR, passwordField).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, login_button).click()
    time.sleep(1)
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
            choice = int(input('which {}? Choose by number: '.format(subject)))
        except ValueError or IndexError:
            print("value is not a number or not between the given range, try again")
        else:
            correct = False
    return choice


def bulk_query_builder(ids, artistid):
    i = 1
    j = 1
    art_id_query = str()
    art_id_query_list = []
    # built the function like this because pixiv doesnt take more than 50 ids
    if i < len(ids):
        for n in ids:
            if j < 50:
                art_id_query += 'ids%5B%5D={}&'.format(n)
                j += 1
                i += 1
            else:
                full_query_for_arts = 'https://www.pixiv.net/ajax/user/{}/profile/illusts?'.format(
                    artistid) + art_id_query + 'work_category=illustManga&is_first_page=0&lang=en'
                art_id_query_list.append(full_query_for_arts)
                art_id_query = ''
                j = 1
                i += 1
        full_query_for_arts = 'https://www.pixiv.net/ajax/user/{}/profile/illusts?'.format(
            artistid) + art_id_query + 'work_category=illustManga&is_first_page=0&lang=en'
        art_id_query_list.append(full_query_for_arts)
    return art_id_query_list


# def single_query_builder(id):
#     # art_id = id      this link is used to get metadata
#     # query = 'https://www.pixiv.net/ajax/user/2188232/profile/illusts?' +  id + 'work_category=illustManga&is_first_page=0&lang=en'
#     url = 'https://i.pximg.net/img-master/img/2022/03/08/00/00/56/{}_p1_master1200.jpg'.format(
#         id)
#     return url


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
    url = 'https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'.format(
        artist_results[choice][choice][1])
    artistid = artist_results[choice][choice][1]
    response = requests.get(url)
    arts_id_list = get_arts_ids(response)
    art_id_query_list = bulk_query_builder(arts_id_list, artistid)
    illustrations = []
    i = 0
    for f in art_id_query_list:
        data = requests.get(f)
        for k, v in data.json()['body']['works'].items():
            art_id = v['id']
            artist_nick = v['userName']
            title = v['title']
            url = format_link_to_download(v['url'])
            illustration = {
                i:
                [
                    art_id,
                    title,
                    url,
                    artist_nick,
                ]
            }
            i += 1
            illustrations.append(illustration)
    return illustrations


def bulk_download(list):
    try:
        choice_list = []
        while True:
            choice_list.append(
                int(input("Please select which ilustration you wanna download: ")))
    except:
        for i in choice_list:
            for k, v in list[i].items():
                path = v[3]+'/'
                img_data = requests.get(
                    v[2], headers={'Referer': 'https://www.pixiv.net/'}, stream=True).content
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, v[1]+'.jpg'), 'wb') as f:
                    f.write(img_data)


def all_download(userid):
    print("downloading.....")
    url = 'https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'.format(
        userid)
    response = requests.get(url)
    arts_id_list = get_arts_ids(response)
    art_id_query_list = bulk_query_builder(arts_id_list, userid)
    illustrations = []
    i = 0
    for f in art_id_query_list:
        data = requests.get(f)
        for k, v in data.json()['body']['works'].items():
            art_id = v['id']
            artist_nick = v['userName']
            title = v['title']
            url = format_link_to_download(v['url'])
            illustration = {
                i:
                [
                    art_id,
                    title,
                    url,
                    artist_nick,
                ]
            }
            i += 1
            illustrations.append(illustration)
    for count, i in enumerate(illustrations):
        path = i[count][3]+'/'
        print(i[count][2])
        img_data = requests.get(
            i[count][2], headers={'Referer': 'https://www.pixiv.net/'}, stream=True).content
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, i[count][1]+'.jpg'), 'wb') as f:
            f.write(img_data)
            count += 1


def single_download(artid):
    print("downloading...")
    metadata_url = 'https://www.pixiv.net/ajax/user/18096447/profile/illusts?ids%5B%5D={}&work_category=illustManga&is_first_page=0&lang=en'.format(
        artid)
    data = requests.get(metadata_url)
    json_data = data.json()['body']['works'][artid]
    art_id = json_data['id']
    artist_nick = json_data['userName']
    title = json_data['title']
    url = format_link_to_download(json_data['url'])
    path = 'illustrations/'+artist_nick
    img_data = requests.get(
        url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True).content
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, title+'.jpg'), 'wb') as f:
        f.write(img_data)
