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
    single_download(artid)


cli.add_command(all)
cli.add_command(single)


if __name__=='__main__':
    cli()

