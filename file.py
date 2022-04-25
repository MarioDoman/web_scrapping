import os
from datetime import date

def file_exists(file):
    return os.path.isfile(file)

def today_file_name():
    return f'first_100_crypto_{date.today()}.txt'