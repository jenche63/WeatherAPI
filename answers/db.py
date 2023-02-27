import os
import sqlite3
import logging
import time
from datetime import datetime

logging.basicConfig(filename='weather.log', encoding='utf-8', level=logging.INFO)
start_time = time.time()
logging.info(f'start job at {start_time}')

conn = sqlite3.connect('weather.db')

print("Opened database successfully")
conn.execute('''
    CREATE TABLE IF NOT EXISTS weather (
	station_id TEXT NOT NULL,
	date DATE NOT NULL,
   	max_temp FLOAT DEFAULT -9999,
	min_temp FLOAT DEFAULT -9999,
	precipitation FLOAT DEFAULT -9999,
	PRIMARY KEY (station_id, date)
);''')
print("Table weather created successfully")

date_files = {}
count = 0
for file in os.listdir("./code-challenge-template/wx_data"):
    if file.endswith(".txt"):
        date_files[file]= os.path.join("./code-challenge-template/wx_data", file)

for k, v in date_files.items():
    station_id = k[:-4]  # parse the station id
    with open(v) as f:
        lines = f.readlines()

    for l in lines:
        record = l.strip().split('\t')
        date = datetime.strptime(record[0],'%Y%m%d').date()
        max_temp = float(record[1])/10
        min_temp = float(record[2])/10
        precipitation = float(record[3])/10
        
        insert_str = f"INSERT INTO weather (station_id,date,max_temp,min_temp,precipitation) \
        VALUES ('{station_id}', '{date}', {max_temp}, {min_temp}, {precipitation})"
        try:
            conn.execute(insert_str)   # in case of duplications for primary keys, the insert will fail
            # print(insert_str)
        except sqlite3.IntegrityError as e:
            conn.rollback()
            print(f"{insert_str} failed!")
            print(str(e))
        count += 1
    conn.commit()

conn.close()

end_time = time.time()
logging.info(f'end job at {end_time}')
job_duration = end_time - start_time
logging.info(f'total # of records inserted: {count}')
logging.info(f'job duration: {job_duration}')