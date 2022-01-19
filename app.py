from flask import Flask, Blueprint, render_template, jsonify, send_from_directory, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
marshmallow = Marshmallow(app)

cors = CORS(
    app,
    resources={r"/api/*"},
)

frontend = Blueprint("frontend", __name__,
    static_folder='static/frontend',
    static_url_path='/'
)

@frontend.route("/news")
def news():
    return frontend.send_static_file("index.html")

app.register_blueprint(frontend)

from models import NewsItem
from apiresources import NewsItemList, RecyclingStreetList, RecyclingEventList

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

media_path = os.path.join(app.root_path, 'media')

@app.route('/media/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    return send_from_directory(media_path, path)

@app.route('/hello')
def etag_post():
    some_response = render_template('impressum.html')
    some_response = make_response(some_response)
    some_response.add_etag()
    return some_response.make_conditional(request)

def etag_pre():
    some_response = make_response()
    some_response.set_etag('the-etag')
    some_response.make_conditional(request)
    if some_response.status_code == 304:
        return some_response
    some_response =  do_expensive_stuff()
    some_response.set_etag('the-etag')
    return some_response

api.add_resource(NewsItemList, '/api/newsitems')
api.add_resource(RecyclingStreetList, '/api/recycling/streets')
api.add_resource(RecyclingEventList, '/api/recycling/street/<street_id>/events')

if __name__ == '__main__':
    app.run()