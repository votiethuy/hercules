# Hercules

Program that can be used to download data from multiple sources and protocols to local disk

## Dependency

- Python 3.6

## Instruction

### Virtualenv

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
pip3 install -r requirements.txt
```

For deactivate

```bash
deactivate
```

### TEST

```bash
python3 setup.py test
```

### Example

```bash
python3 hercules/cli.py download https://i.pinimg.com/564x/07/ae/16/07ae164da80a7168c59a01c41bfdb74a.jpg
```

Download from FTP

```bash
python3 hercules/cli.py download ftp://206.189.83.200/files/agoda.jpg
```

Download from SFTP

```bash
python3 hercules/cli.py download sftp://206.189.83.200//home/agoda_sftp_user/agoda.jpg
```
