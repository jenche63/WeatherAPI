import os
import sqlite3

conn = sqlite3.connect('weather.db')

print("Opened database successfully")
target_table = 'weather_stat'
conn.execute(f'''
    CREATE TABLE IF NOT EXISTS {target_table} (
	station_id TEXT NOT NULL,
    year INT NOT NULL,
   	avg_max_temp FLOAT,
	avg_min_temp FLOAT,
	sum_precipitation FLOAT,
	PRIMARY KEY (station_id, year)
);''')
print(f"Table {target_table} created successfully")

cursor = conn.cursor()


stmt = """
SELECT
    station_id,
    strftime('%Y',date) As year,
    AVG(max_temp) AS avg_max_temp,
    AVG(min_temp) AS avg_min_temp,
    SUM(precipitation) AS sum_precipitation
    FROM weather
WHERE
    max_temp != -999.9
    AND min_temp != -999.9
    AND precipitation != -999.9
GROUP BY
    station_id,
    year
"""

cursor.execute(stmt)

data = cursor.fetchall()
fields = ','.join('?' for desc in cursor.description)
stmt = "insert into {} values ({})".format(target_table, fields)
cursor.executemany(stmt, data)
conn.commit()
conn.close()