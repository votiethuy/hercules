import pytest
import os

from hercules import cli



def test_download_http():
    cli.download_http("https://i.pinimg.com/564x/07/ae/16/07ae164da80a7168c59a01c41bfdb74a.jpg")
    assert os.path.exists("downloads/07ae164da80a7168c59a01c41bfdb74a.jpg")

