from peewee import *
import datetime
from time import sleep
from urllib.request import urlopen

db = SqliteDatabase('database.db')

period = 30

class NetworkConnection(Model):

    internet_on = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.today)

    class Meta:
        database = db
        db_table = 'network_connection'

NetworkConnection.create_table()

def internet_on(url: str = 'https://www.google.com/', timeout: int = 10):
    try:
        resp = urlopen(url=url, timeout=timeout)
        return True
    except Exception as e:
        error_str = str(e)
        if "Too Many Requests" in error_str:
            return True
        return False

while True:
    try:
        is_internet_on = internet_on(timeout=1)
        created = datetime.datetime.now()
        network_connection = NetworkConnection.create(internet_on=is_internet_on, created=created)
    except Exception as e:
        print(e)
    sleep(period)
