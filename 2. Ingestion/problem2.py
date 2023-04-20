'''
Approach:
Here we are using python to create wrapper script to perform ETL operations.
As first step we are connecting to postgreSQL database and then looping thru each weather data file into dictionary and splitting the line into columns and extracting the values of each column and then ignoring duplicates and inserting into weather data table and closing the connection created and print the no of records ingestion towards the end of the process. 
'''
import os
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="some_host",
    database="some_database",
    user="some_username",
    password="some_password"
)

cur = conn.cursor()

for filename in os.listdir("wx_data"):
    with open(os.path.join("wx_data", filename), "r") as f:
        next(f)

        for line in f:
            columns = line.strip().split("\t")

            date_str = columns[0]
            max_temp = float(columns[1]) / 10.0 if columns[1] != "-9999" else None
            min_temp = float(columns[2]) / 10.0 if columns[2] != "-9999" else None
            precipitation = float(columns[3]) / 10.0 if columns[3] != "-9999" else None

            date = datetime.strptime(date_str, "%Y%m%d").date()

            cur.execute(
                "INSERT INTO weather_data (station_id, date, max_temp, min_temp, precipitation) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (filename[:-4], date, max_temp, min_temp, precipitation)
            )

conn.commit()

cur.close()
conn.close()

total_records = cur.rowcount
print(f"Total records ingested: {total_records}")

