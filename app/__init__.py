#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
import sys

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

    return app


app = create_app()
db = SQLAlchemy(app)
import prob.models
if db.session.query(prob.models.Prob).filter_by(title='signup').first() is None:
    p = Prob()
    p.title = "signup"
    p.score = "0"
    p.key = ""
    db.session.add(p)
    db.session.commit()

import account.models
import main.models
import prob.models
from account.models import *
from main.models import *
from prob.models import *

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


def user_session():
    try:
        session['login']
    except KeyError:
        session['login'] = False
        session['userid'] = "Guest"
        session['nickname'] = "Guest"
        session['admin'] = False
    return session


@app.context_processor
def template_processor():
    user_data = user_session()
    return dict(userid=user_data['userid'],
                nickname=user_data['nickname'])


@app.template_filter('torank')
def index_rank(index):
    return int(index) + 1
