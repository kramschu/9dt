from flask import Blueprint, Flask, jsonify
from game_api import game_api
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.register_blueprint(game_api, url_prefix='/drop_token')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///components/db/drop_token.db' #database file (sqlite) this will create file in the project folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()


@app.route('/')
def info():
    return jsonify(message="This is the drop_token api")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
