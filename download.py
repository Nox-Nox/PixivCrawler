from pixiv_functions import*
import requests
import click


def download_all_by_artist_id(user_id):
    url = 'https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'.format(
        user_id)
    response = requests.get(url)
    arts_id_list = get_arts_ids(response)
    art_id_query_list = bulk_query_builder(arts_id_list)
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
    all_download(illustrations)

@click.command()
@click.option('--artid')
def download_art_by_id(artid):
    print("downloading...")
    url = single_query_builder(artid)
    path = 'illustrations/'
    img_data = requests.get(url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True).content
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'illustration.jpg'), 'wb') as f:
        f.write(img_data)


if __name__=='__main__':
    download_art_by_id()


