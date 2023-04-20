For this we are using Flask web framework to create the REST API.
Here is the high level steps involved for this

1.Create a Flask application instance and define the routes for the API endpoints /api/weather and /api/weather/stats.
2.Define a function to handle the GET requests for each endpoint.
3.Use SQLAlchemy to interact with the database and retrieve the required data based on the query parameters.
4.Use Flask-RESTful to paginate the response data.
5.Use Flask-SwaggerUI to create the Swagger documentation for the API.
6.Write unit tests using pytest.

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract, func
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'some_database_uri'
db = SQLAlchemy(app)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(8))
    station = db.Column(db.String(50))
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

class WeatherDataSchema(Schema):
    id = fields.Integer()
    date = fields.String()
    station = fields.String()
    max_temp = fields.Float()
    min_temp = fields.Float()
    precipitation = fields.Float()

@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    query = WeatherData.query
    if 'date' in request.args:
        query = query.filter_by(date=request.args.get('date'))
    if 'station' in request.args:
        query = query.filter_by(station=request.args.get('station'))
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = query.paginate(page=page, per_page=per_page)
    schema = WeatherDataSchema(many=True)
    return jsonify(schema.dump(data.items))

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    year = request.args.get('year')
    station = request.args.get('station')
    if year:
        query = db.session.query(WeatherData.station,
                                  func.avg(WeatherData.max_temp),
                                  func.avg(WeatherData.min_temp),
                                  func.sum(WeatherData.precipitation)
                                  ).filter(extract('year', WeatherData.date) == year)
    else:
        query = db.session.query(WeatherData.station,
                                  func.avg(WeatherData.max_temp),
                                  func.avg(WeatherData.min_temp),
                                  func.sum(WeatherData.precipitation)
                                  )
    if station:
        query = query.filter_by(station=station)
    data = query.group_by(WeatherData.station).all()
    result = []
    for row in data:
        result.append({
            'station': row[0],
            'avg_max_temp': round(row[1], 2) if row[1] else None,
            'avg_min_temp': round(row[2], 2) if row[2] else None,
            'total_precipitation': round(row[3]/10, 2) if row[3] else None
        })
    return jsonify(result)
