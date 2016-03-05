#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from flask import Flask, session
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.contrib.fixers import ProxyFix

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


app = create_app()
db = SQLAlchemy(app)

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
        session['admin'] = False
    return session


@app.template_filter('torank')
def index_rank(index):
    return int(index) + 1


# for error 'mysql server gone'
@app.teardown_request
def refresh_db(exception=None):
    db.session.remove()
    db.create_scoped_session()


def init_db():
    db.session.rollback()

    u = User()
    u.userid = "admin"
    u.userpw = "test"
    u.score = 0
    u.nickname = "Administrator"
    u.is_admin = True
    u.active = False
    db.session.add(u)
    db.session.commit()

    c = Category()
    c.title = "Signup"
    c.active = False
    db.session.add(c)
    db.session.commit()

    p = Prob()
    p.title = "Signup"
    p.key = "Thank You For Signup"
    p.active = False
    p.maker_id = u.id
    p.category = c
    p.category_id = c.id
    c.prob.append(p)
    db.session.add(p)
    db.session.commit()

    u = User()
    u.userid = "asdf"
    u.userpw = "asdf"
    u.score = 0
    u.nickname = "fortest"
    u.is_admin = False
    u.success_prob.append(p)
    db.session.add(u)
    db.session.commit()

    # Add Extra Category
    p = Category()
    p.title = "Pwnable"
    db.session.add(p)

    p = Category()
    p.title = "Web"
    db.session.add(p)

    p = Category()
    p.title = "Network"
    db.session.add(p)

    p = Category()
    p.title = "Forensic"
    db.session.add(p)

    p = Category()
    p.title = "ETC"
    db.session.add(p)

    db.session.commit()

    import os
    if not os.path.exists('./prob/prob_files'):
        print "make ./prob/prob_files directory!"
    if not os.path.exists('./prob/prob_images'):
        print "make ./prob/prob_images directory!"
