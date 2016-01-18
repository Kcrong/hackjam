#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

from . import views