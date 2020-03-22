from flask import Flask, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
marshmallow = Marshmallow(app)

from models import NewsItem
from apiresources import NewsItemList

@app.route('/')
def index():
    return render_template('index.html')

media_path = os.path.join(app.root_path, 'media')

@app.route('/media/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    return send_from_directory(media_path, path)

api.add_resource(NewsItemList, '/api/newsitems')

if __name__ == '__main__':
    app.run()