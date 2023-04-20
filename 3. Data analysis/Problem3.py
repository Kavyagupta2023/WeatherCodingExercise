'''
We are using a python wrapper script to create and calculate statistics and load into weather statistics table. All the sql transformations and bundled into python code. 
'''
import sqlite3

conn = sqlite3.connect('weather.db')
c = conn.cursor()

query = '''
    SELECT substr(date, 1, 4) AS year,
           station_id,
           avg(max_temp_c) AS avg_max_temp_c,
           avg(min_temp_c) AS avg_min_temp_c,
           sum(precipitation_cm) AS total_precipitation_cm
    FROM weather
    WHERE max_temp_c != -9999 AND min_temp_c != -9999 AND precipitation_cm != -9999
    GROUP BY year, station_id
'''

for row in c.execute(query):
    year, station_id, avg_max_temp_c, avg_min_temp_c, total_precipitation_cm = row
    c.execute('''
        INSERT INTO weather_stats (year, station_id, avg_max_temp_c, avg_min_temp_c, total_precipitation_cm)
        VALUES (?, ?, ?, ?, ?)
    ''', (year, station_id, avg_max_temp_c, avg_min_temp_c, total_precipitation_cm))

conn.commit()
conn.close()
