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


@app.context_processor
def template_processor():
    user_data = user_session()
    return dict(userid=user_data['userid'],
                nickname=user_data['nickname'])


@app.template_filter('torank')
def index_rank(index):
    return int(index) + 1


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
        os.makedirs('./prob/prob_files', mode=777)
    if not os.path.exists('./prob/prob_images'):
        os.makedirs('./prob/prob_images', mode=777)

