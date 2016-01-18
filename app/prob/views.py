#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from . import prob_blueprint


@prob_blueprint.route('/list')
def list():
    return render_template('prob/prob.html')


