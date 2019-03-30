import click
import requests
import os
import settings
from tqdm import tqdm


@click.group()
def main():
    """
    Simple CLI for downloading data from multiple sources and protocols to local disk.
    """
    pass

@main.command()
@click.argument('url')
def download(url):
    """This download to the configuration folder and return path file corresponding to the given url"""
    r = requests.get(url)
    file_name = os.path.basename(url)
    path = os.path.join(settings.FOLDER, file_name)
    with open(path, 'wb') as f:
        f.write(r.content)

    click.echo(r.status_code)
    click.echo(r.headers['content-type'])
    click.echo(r.encoding)

if __name__ == "__main__":
    main()