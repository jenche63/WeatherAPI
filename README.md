# WeatherAPI
### weather data records from 1985-01-01 to 2014-12-31
### Problem 1 - Data Modeling
### Problem 2 - Ingestion
### Problem 3 - Data Analysis
-------------------------
Inside the answers folder, db.py and db_stats.py are called to generate weather and weather_stats table inside weather.db. The github has limitation of 100mb to upload. So I didn't upload the weather.db. Duplicate issue and logging are all addressed in my code above.

### Problem 4 - REST API
--------------------
Flask framework are used and app.py inside the answer folder to generate the following GET endpoints:

/api/weather

/api/weather/stats

Inside the templates folder there are weather.html and weather_stat.html, together with the app.py to filter the response by date and station ID (where present) using the query string. Inside the browser, please type the following links to check:

http://127.0.0.1:5000/weather?station_id=USC00110072

http://127.0.0.1:5000/weather?station_id=USC00110072&date=19850101

http://127.0.0.1:5000/weather?date=19850101

http://127.0.0.1:5000/weather

http://127.0.0.1:5000/weather/stats?station_id=USC00110072

http://127.0.0.1:5000/weather/stats?station_id=USC00110072&year=1986

http://127.0.0.1:5000/weather/stats?year=1986

Please check the following Swagger/OpenAPI endpoint that provides automatic documentation of my API.
https://app.swaggerhub.com/apis/jenche63/weather_api/0.1
https://app.swaggerhub.com/apis/jenche63/weather_stats_api/0.1

