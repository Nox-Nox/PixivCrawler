from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pixiv_functions import*


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
    outer_correct = True
    while outer_correct:
        picked_choice = choice('artist')
        if 0 <= picked_choice <= len(artist_results):
            print(artist_results[picked_choice][picked_choice][0],
                  ' ', artist_results[picked_choice][picked_choice][1])
            arts_of_chosen_artist = get_arts_of_chosen_artist(
                artist_results, picked_choice)
            display(arts_of_chosen_artist)
            inner_correct = True
            while inner_correct:
                choice_str = input(
                    'Do you wanna download one/more(m) illustrations or all(a) of them? ')
                if choice_str == 'm':
                    bulk_download(arts_of_chosen_artist)
                    inner_correct = False
                elif choice_str == 'a':
                    all_download(arts_of_chosen_artist)
                    inner_correct = False
                else:
                    print(
                        'Please select a valid option, "m" for one/more illustration, "a" to get all illustrations')
            outer_correct = False
        else:
            print("please choose a valid value between the given options: ")
