import click
import requests
import os
import sys
from tqdm import tqdm
import math
from urllib.parse import urlparse
import ftplib
from contextlib import closing
import paramiko

FOLDER = os.environ.get("FOLDER_DOWNLOAD", "downloads") # if not set path to download it will download to downloads folder

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

def promt_user():
    username = click.prompt("Username or enter '-' to skip")
    if username == "-":
        username = None
        password = None
    else:
        password = click.prompt("Password", hide_input=True)
    return username, password

def download_ftp(host,remote_path, ftp_user, ftp_password):
    """Download protocal FTP"""
    file_name = os.path.basename(remote_path)
    local_filename = os.path.join(FOLDER, file_name)
    with closing(ftplib.FTP()) as ftp:
        try:
            ftp.connect(host, timeout=30*5)
            if ftp_user:
                ftp.login(ftp_user, ftp_password)
                ftp.set_pasv(True)
            else:
                ftp.login()
            with open(local_filename, 'w+b') as f:
                total = ftp.size(remote_path)
                with tqdm(total=total,unit_scale=True,desc=remote_path,miniters=1,file=sys.stdout,leave=True) as pbar:
                    def cb(data):
                        pbar.update(len(data))
                        f.write(data)
                res = ftp.retrbinary('RETR %s' % remote_path, cb)
                if not res.startswith('226'):
                    click.echo('Downloaded of file {0} is not compile.'.format(remote_path))
                    click.echo(res)
                    os.remove(local_filename)
                    return None
            click.echo("Downloaded {}".format(local_filename))
            return local_filename
        except Exception as e:
            click.echo('Error during download from FTP: {}'.format(str(e)))
            os.remove(local_filename)
            return None
        

def download_sftp(host,remote_path,username,password):
    """Download protocal SFTP"""
    file_name = os.path.basename(remote_path)
    local_filename = os.path.join(FOLDER, file_name)
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_path, local_filename)
        click.echo("Downloaded {}".format(local_filename))
        return local_filename
    except Exception as e:
        click.echo('Error during download from FTP: {}'.format(str(e)))
        os.remove(local_filename)
        return None
    finally:
        sftp.close()
        transport.close()
    

def download_http(url):
    """Download protocal http"""
    r = requests.get(url, stream=True)
    file_name = os.path.basename(url)
    local_filename = os.path.join(FOLDER, file_name)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(local_filename, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        os.remove(local_filename)
        click.echo("ERROR, something went wrong")
        return None
    click.echo("Downloaded {}".format(local_filename))
    return local_filename

def download_url(url):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
    click.echo("Start downloading {} ...".format(url))
    if uri.scheme == 'http' or uri.scheme == 'https':
        return download_http(url)
    elif uri.scheme == 'ftp':
        username, password = promt_user()
        return download_ftp(uri.netloc, uri.path, username, password)
    elif uri.scheme == 'sftp':
        username, password = promt_user()
        return download_sftp(uri.netloc, uri.path, username, password)
    else:
        click.echo("{} not supported".format(uri.scheme))
        return None

@main.command()
@click.argument('url')
def download(url):
    """This download to the configuration folder and return path file corresponding to the given url"""
    download_url(url)

@main.command()
@click.argument('urls_file', envvar='SRC', type=click.File('r'))
def download_from_urls_file(urls_file):
    """This download from urls_file"""
    list_urls_data = urls_file.read()
    list_url = list_urls_data.split('\n')
    for url in list_url:
        download_url(str(url))
    click.echo(list_url)


if __name__ == "__main__":
    main()