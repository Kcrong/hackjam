#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

prob_blueprint = Blueprint('prob', __name__)

from . import views
