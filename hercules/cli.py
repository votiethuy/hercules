import click
import requests
import os
import settings
from tqdm import tqdm
import math
from urllib.parse import urlparse
import ftplib
from contextlib import closing

@click.group()
def main():
    """
    Simple CLI for downloading data from multiple sources and protocols to local disk.
    """
    pass

@main.command()
def config():
    """This create config file for usage later"""
    click.echo("Config Done")

def download_ftp(host,remote_path):
    """Download protocal FTP"""
    file_name = os.path.basename(remote_path)
    local_filename = os.path.join(settings.FOLDER, file_name)
    ftp_user = click.prompt("FTP username or enter '-' to skip")
    if ftp_user == "-":
        ftp_user = None
        ftp_password = None
    else:
        ftp_password = click.prompt("FTP password", hide_input=True)
    with closing(ftplib.FTP()) as ftp:
        try:
            ftp.connect(host, timeout=30*5)
            if ftp_user:
                ftp.login(ftp_user, ftp_password)
                ftp.set_pasv(True)
            else:
                ftp.login()
            with open(local_filename, 'w+b') as f:
                res = ftp.retrbinary('RETR %s' % remote_path, f.write)
                if not res.startswith('226'):
                    click.echo('Downloaded of file {0} is not compile.'.format(remote_path))
                    click.echo(res)
                    os.remove(local_filename)
                    return None
            return local_filename
        except Exception as e:
            click.echo('Error during download from FTP {}'.format(str(e)))
            return None
        

def dowload_sftp(url,username,password):
    """Download protocal SFTP"""
    click.echo("SFTP not supported")

def download_http(url):
    """Download protocal http"""
    r = requests.get(url, stream=True)
    file_name = os.path.basename(url)
    local_filename = os.path.join(settings.FOLDER, file_name)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(local_filename, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)

    if total_size != 0 and wrote != total_size:
        click.echo("ERROR, something went wrong")

@main.command()
@click.argument('url')
def download(url):
    """This download to the configuration folder and return path file corresponding to the given url"""
    uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
    click.echo("Start downloading {} ...".format(url))
    if uri.scheme == 'http' or uri.scheme == 'https':
        download_http(url)
    elif uri.scheme == 'ftp':
        download_ftp(uri.netloc, uri.path)


if __name__ == "__main__":
    main()