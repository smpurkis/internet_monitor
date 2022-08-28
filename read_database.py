from pathlib import Path
import pandas as pd
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Downperiod:
    start_datetime: datetime
    end_datetime: datetime
    duration: timedelta

db_name = list(Path().glob("*.db"))[0].name
conn = sqlite3.connect(db_name)


def read_database(conn):
    df = pd.read_sql("SELECT * FROM network_connection", conn).convert_dtypes()
    df.internet_on = df.internet_on.astype(bool)
    df.created = pd.to_datetime(df.created, infer_datetime_format=True)
    return df

df = read_database(conn)
print(df)


def extract_downtimes(df: pd.DataFrame):
    data = df.to_dict("records")
    down_periods = []

    start_datetime = None
    end_datetime = None
    in_downperiod = False
    for row in data:
        if in_downperiod:
            if row["internet_on"]:
                end_datetime = row["created"]
                in_downperiod = False
                down_period = Downperiod(start_datetime, end_datetime, end_datetime - start_datetime)
                down_periods.append(down_period)
            else:
                continue
        else:
            if row["internet_on"]:
                continue
            else:
                start_datetime = row["created"]
                in_downperiod = True
    for dp in down_periods:
        print(dp)
    
extract_downtimes(df)