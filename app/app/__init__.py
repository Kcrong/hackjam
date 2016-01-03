#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

app_blueprint = Blueprint('app', __name__)

from . import views