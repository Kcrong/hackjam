#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, manager
from app import init_db


@manager.command
def run():
    app.run(host='0.0.0.0', debug=True)


@manager.command
def db_init():
    init_db()
    print "Success to Generate db init data."


if __name__ == "__main__":
    manager.run()
