/*
Approach:
Creating a new table to record the  calculated weather statistics for each year and station.

This table has columns for the weather station ID, the year, and the calculated statistics for that station and year.
*/
CREATE TABLE weather_stats (
  year INTEGER NOT NULL,
  station_id TEXT NOT NULL,
  avg_max_temp_c REAL,
  avg_min_temp_c REAL,
  total_precipitation_cm REAL,
  PRIMARY KEY (year, station_id)
);



