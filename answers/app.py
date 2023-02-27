import os
from flask import Flask, render_template, request, abort, url_for, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'weather.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ROWS_PER_PAGE = 6 # pagination

class Weather(db.Model):
    station_id = db.Column(db.String(20), primary_key=True)
    date = db.Column(db.String(20), primary_key=True)
    max_temp = db.Column(db.Float, nullable=True)
    min_temp = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    def __repr__(self):
        return f'<Weather {self.station_id} {self.date}>'

class WeatherStat(db.Model):
    station_id = db.Column(db.String(20), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    sum_precipitation = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Weather {self.station_id} {self.year}>'

# @app.route('/')
# def index():
    
#     return render_template('weather_no.html'), 200

@app.route('/weather',methods=['GET','POST'])
def weather():
    if request.method == "GET":
        args = request.args
        station_id = None
        date = None
        if "station_id" in args:
            station_id = args.get("station_id")
        if "date" in args:
            date = args.get("date")
        page = request.args.get('page', 1, type=int)
        data = None
        if station_id is not None and date is not None:
            data = Weather.query.filter_by(station_id=station_id, date=date).paginate(page=page, per_page=ROWS_PER_PAGE)
        elif station_id is not None:
            data = Weather.query.filter_by(station_id=station_id).paginate(page=page, per_page=ROWS_PER_PAGE)
        elif date is not None:
            data = Weather.query.filter_by(date=date).paginate(page=page, per_page=ROWS_PER_PAGE)
        else:
            data = Weather.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        if data is not None:
            # return jsonify(data), 200
            return render_template('weather.html', data=data, station_id=station_id, date=date), 200
        else:
            return "No Record Found!", 404
    

@app.route('/weather/stats', methods=['GET','POST'])
def weather_stats():
    if request.method == "GET":
        args = request.args
        station_id = None
        year = None
        if "station_id" in args:
            station_id = args.get("station_id")
        if "year" in args:
            year = args.get("year")
        page = request.args.get('page', 1, type=int)
        data = None
        if station_id is not None and year is not None:
            data = WeatherStat.query.filter_by(station_id=station_id, year=year).paginate(page=page, per_page=ROWS_PER_PAGE)
        elif station_id is not None:
            data = WeatherStat.query.filter_by(station_id=station_id).paginate(page=page, per_page=ROWS_PER_PAGE)
        elif year is not None:
            data = WeatherStat.query.filter_by(year=year).paginate(page=page, per_page=ROWS_PER_PAGE)
        else:
            data = WeatherStat.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        if data is not None:
            # return jsonify(data), 200
            return render_template('weather_stat.html', data=data, station_id=station_id, year=year), 200
        else:
            return "No Record Found!", 404


if __name__=='__main__':
    app.run(debug=True)