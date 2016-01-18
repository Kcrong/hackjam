#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

prob_blueprint = Blueprint('prob', __name__, template_folder='../templates/prob/')

from . import views
