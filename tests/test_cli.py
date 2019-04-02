import pytest
import os

from hercules import cli

@pytest.mark.parametrize('url, expected', [("https://i.pinimg.com/564x/07/ae/16/07ae164da80a7168c59a01c41bfdb74a.jpg", "downloads/07ae164da80a7168c59a01c41bfdb74a.jpg")])
def test_download_url(url, expected):
    local_file_name = cli.download_url(url)
    assert local_file_name == expected
    assert os.path.exists(expected)
    os.remove(expected) # clean test data download

@pytest.mark.parametrize('url, expected', [("https://i.pinimg.com/564x/07/ae/16/07ae164da80a7168c59a01c41bfdb74a.jpg", "downloads/07ae164da80a7168c59a01c41bfdb74a.jpg")])
def test_download_http(url, expected):
    local_file_name = cli.download_http(url)
    assert local_file_name == expected
    assert os.path.exists(expected)
    os.remove(expected) # clean test data download
    

@pytest.mark.parametrize('host,remote_path, ftp_user, ftp_password, expected', [('206.189.83.200','files/agoda.jpg','agoda_ftp_user','GGaPbZ5F2Nqrk8Nk','downloads/agoda.jpg')])
def test_download_ftp(host,remote_path, ftp_user, ftp_password, expected):
    local_file_name = cli.download_ftp(host,remote_path, ftp_user, ftp_password)
    assert local_file_name == expected
    assert os.path.exists(expected)
    os.remove(expected) # clean test data download

@pytest.mark.parametrize('host,remote_path, username, password, expected', [('206.189.83.200','/home/agoda_sftp_user/agoda.jpg','agoda_sftp_user','672ervpWW43WWTnv','downloads/agoda.jpg')])
def test_download_sftp(host,remote_path, username, password, expected):
    local_file_name = cli.download_sftp(host,remote_path, username, password)
    assert local_file_name == expected
    assert os.path.exists(expected)
    os.remove(expected) # clean test data download

