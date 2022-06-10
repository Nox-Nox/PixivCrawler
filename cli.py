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
    all_download(userid)


@click.command('single', short_help='to download a single illustration, type/paste the artwork id')
@click.option('--artid', help="paste the id of the art found in the url")
@click.argument('artid')
def single(artid):
    print("downloading...")
    url = 'https://www.pixiv.net/ajax/user/18096447/profile/illusts?ids%5B%5D={}&work_category=illustManga&is_first_page=0&lang=en'.format(artid)
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

