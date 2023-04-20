For this we are using Flask web framework to create the REST API.
Here is the high level steps involved for this

1.Create a Flask application instance and define the routes for the API endpoints /api/weather and /api/weather/stats.
2.Define a function to handle the GET requests for each endpoint.
3.Use SQLAlchemy to interact with the database and retrieve the required data based on the query parameters.
4.Use Flask-RESTful to paginate the response data.
5.Use Flask-SwaggerUI to create the Swagger documentation for the API.
6.Write unit tests using pytest.


from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTFUL_API_DOC_EXPANSION'] = 'list'
app.config['RESTFUL_MASK_SWAGGER'] = False
app.config['RESTFUL_PAGINATION'] = True
app.config['RESTFUL_DEFAULT_PAGE'] = 1
app.config['RESTFUL_DEFAULT_PAGE_SIZE'] = 10

api = Api(app)
db = SQLAlchemy(app)
CORS(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    '/swagger',
    '/static/swagger.json',
    config={
        'app_name': 'Weather API'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(10))
    date = db.Column(db.Date)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

    def __repr__(self):
        return f'<Weather {self.id}>'


weather_parser = reqparse.RequestParser()
weather_parser.add_argument('station_id', type=str)
weather_parser.add_argument('start_date', type=inputs.date)
weather_parser.add_argument('end_date', type=inputs.date)
weather_parser.add_argument('page', type=int)
weather_parser.add_argument('per_page', type=int)


weather_fields = {
    'id': fields.Integer,
    'station_id': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
    'max_temp': fields.Float,
    'min_temp': fields.Float,
    'precipitation': fields.Float
}


class WeatherResource(Resource):
    @marshal_with(weather_fields)
    def get(self):
        args = weather_parser.parse_args()

        # Query filters
        filters = []
        if args.station_id:
            filters.append(Weather.station_id == args.station_id)
        if args.start_date:
            filters.append(Weather.date >= args.start_date)
        if args.end_date:
            filters.append(Weather.date <= args.end_date)

        # Query results
        results = Weather.query.filter(*filters).paginate(
            page=args.page,
            per_page=args.per_page
        )

        return results.items


stats_parser = reqparse.RequestParser()
stats_parser.add_argument('start_date', type=inputs.date)
stats_parser.add_argument('end_date', type=inputs.date)
stats_parser.add_argument('page', type=int)
stats_parser.add_argument('per_page', type=int)


stats_fields = {
    'station_id': fields.String,
    'year': fields.Integer,
    '