#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import create_app, manager
from app.models import *

app = create_app()


@manager.command
def run():
    app.run(host='0.0.0.0', debug=True)


@manager.command
def init_db():
    u = User()
    u.nickname = 'admin'
    u.userid = 'Administrator'
    u.userpw = 'Administrator'
    u.active = False

    p = Prob()
    p.title = 'signup'
    p.key = 'Hello World'
    p.active = False
    p.maker = u

    u.success_prob = [p]

    db.session.add_all([u, p])
    db.session.commit()


if __name__ == "__main__":
    manager.run()
