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
python3 -m unittest discover -s tests
```

### Example

```bash
python3 hercules/cli.py download https://i.pinimg.com/564x/07/ae/16/07ae164da80a7168c59a01c41bfdb74a.jpg
```

public FTP host for testing

```code
FTP URL: ftp.dlptest.com or ftp://ftp.dlptest.com/
FTP User: dlpuser@dlptest.com
Password: VADPRDqid4TaB0r5a2B0n9wLp
```

```bash
python3 hercules/cli.py download ftp://ftp.dlptest.com/ftp/07ae164da80a7168c59a01c41bfdb74a.jpg
```
