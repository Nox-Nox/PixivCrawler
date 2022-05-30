from pixiv_functions import*
import requests
import click


@click.group()
def cli():
    pass


@click.command('all', short_help='to download all illustrations of an artist, type/paste the artist id')
@click.option('--userid', help="paste user id number found in the url")
@click.argument('userid')
def all(userid):
    print("downloading.....")
    url = 'https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'.format(
        userid)
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


@click.command('single', short_help='to download a single illustration, type/paste the artwork id')
@click.option('--artid', help="paste the id of the art found in the url")
@click.argument('artid')
def single(artid):
    print("downloading...")
    url = single_query_builder(artid)
    path = 'illustrations/'
    img_data = requests.get(url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True).content
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'illustration.jpg'), 'wb') as f:
        f.write(img_data)


cli.add_command(all)
cli.add_command(single)


if __name__=='__main__':
    cli()

