#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask

app = Flask(__name__)


def create_app():
    from app import app_blueprint
    app.register_blueprint(app_blueprint)
    return app