'''
We are using a python wrapper script to create and calculate statistics and load into weather statistics table. All the sql transformations and bundled into python code. 
'''
import psycopg2

conn = psycopg2.connect(
    host="some_host",
    database="some_database",
    user="some_username",
    password="some_password"
)

cur = conn.cursor()

cur.execute("SELECT DISTINCT station_id FROM weather_data")

for row in cur.fetchall():
    station_id = row[0]

    cur.execute("SELECT DISTINCT EXTRACT(year FROM date) FROM weather_data WHERE station_id = %s", (station_id,))

    for row in cur.fetchall():
        year = int(row[0])

        cur.execute(
            "SELECT AVG(max_temp), AVG(min_temp), SUM(precipitation) FROM weather_data WHERE station_id = %s AND EXTRACT(year FROM date) = %s AND max_temp IS NOT NULL AND min_temp IS NOT NULL AND precipitation IS NOT NULL",
            (station_id, year)
        )
        avg_max_temp, avg_min_temp, total_precipitation = cur.fetchone()

        cur.execute(
            "INSERT INTO weather_statistics (station_id, year, avg_max_temp, avg_min_temp, total_precipitation) VALUES (%s, %s, %s, %s, %s)",
            (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
        )

conn.commit()

cur.close()
conn.close()