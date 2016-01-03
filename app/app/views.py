#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from . import app_blueprint


@app_blueprint.route('/')
def index():
    return render_template('app/index.html')