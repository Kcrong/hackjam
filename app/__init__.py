#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from flask import Flask, redirect, url_for
from flask.ext.login import LoginManager
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
login_manager = LoginManager()


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


app.config.from_pyfile('../config.py')
db.init_app(app)

from .models import *

migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUser

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('account.login'))
