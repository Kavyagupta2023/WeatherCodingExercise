'''
Approach:
Here we are using python to create wrapper script to perform ETL operations.
1. Parse the files in the wx_data directory to extract the weather data records.
2. Check for duplicates by querying the database to see if a record with the same date and station_id already exists. If a record already exists, skip it and move on to the next record.
3. If a record does not exist, insert it into the weather_data table along with the corresponding station_id from the station_data table.

'''
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import datetime

engine = create_engine('sqlite:///weather.db')
Session = sessionmaker(bind=engine)
session = Session()

wx_data_dir = 'wx_data'

start_time = datetime.datetime.now()

for filename in os.listdir(wx_data_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(wx_data_dir, filename)
        with open(filepath, 'r') as f:
            # Loop through each line in the file
            for line in f:
                data = line.strip().split('\t')
                date = datetime.datetime.strptime(data[0], '%Y%m%d').date()
                max_temp = float(data[1]) / 10.0
                min_temp = float(data[2]) / 10.0
                precipitation = float(data[3]) / 10.0

                # Check for duplicates
                exists = session.query(text("EXISTS (SELECT 1 FROM weather_data WHERE date=:date AND station_id=:station_id)")).params(date=date, station_id=filename.split('.')[0]).scalar()

                # If record doesn't exist, insert it into the database
                if not exists:
                    session.execute('INSERT INTO weather_data (date, station_id, max_temp, min_temp, precipitation) VALUES (:date, :station_id, :max_temp, :min_temp, :precipitation)', {'date': date, 'station_id': filename.split('.')[0], 'max_temp': max_temp, 'min_temp': min_temp, 'precipitation': precipitation})

end_time = datetime.datetime.now()

session.commit()
session.close()


num_records = session.query(text('SELECT COUNT(*) FROM weather_data')).scalar()
print(f'Ingestion completed. {num_records} records ingested in {end_time - start_time}.')

