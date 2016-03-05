#!/usr/bin/env python
# -*- coding:utf-8 -*-
from time import time

from flask import Blueprint, request, session, redirect
from werkzeug.exceptions import BadRequestKeyError

prob_blueprint = Blueprint('prob', __name__, template_folder='../templates/prob/')

from . import views
