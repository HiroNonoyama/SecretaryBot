# -*- coding: utf-8 -*-
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'secretary',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)


def register_blueprints(app):
    from views import todos
    app.register_blueprint(todos)

register_blueprints(app)
if __name__ == '__main__':
    app.run()
