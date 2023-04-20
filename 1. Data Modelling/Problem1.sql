*/
Approach:
--------
the weather data records contain information about the date, maximum temperature, minimum temperature, and precipitation. Based on this, we can design a data model to represent the weather data records as follows:

Table: weather_data

date: The date of the weather data record. This is the primary key of the table.
station_id: The ID of the weather station that recorded the data. This is a foreign key that references the station_data table.
max_temp: The maximum temperature for that day in tenths of a degree Celsius.
min_temp: The minimum temperature for that day in tenths of a degree Celsius.
precipitation: The amount of precipitation for that day in tenths of a millimeter.
Table: station_data

Table: station_data

id: The ID of the weather station. This is the primary key of the table.
state: The state where the weather station is located.
city: The city where the weather station is located.

*/

CREATE TABLE station_data (
    id TEXT PRIMARY KEY,
    state TEXT,
    city TEXT
);

CREATE TABLE weather_data (
    date DATE PRIMARY KEY,
    station_id TEXT REFERENCES station_data(id),
    max_temp FLOAT,
    min_temp FLOAT,
    precipitation FLOAT
);
