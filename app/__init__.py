#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()

app = Flask(__name__)
db = SQLAlchemy()


def create_app():
    sys.path.append(app.root_path)
    from .main import main_blueprint
    from .account import account_blueprint
    from .prob import prob_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(account_blueprint, url_prefix='/account')
    app.register_blueprint(prob_blueprint, url_prefix='/prob')

    app.config.from_pyfile('../config.py')
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app


db.init_app(app)

from .models import *

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@app.template_filter('torank')
def index_rank(index):
    return int(index) + 1


