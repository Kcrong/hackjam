#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

account_blueprint = Blueprint('account', __name__, template_folder='../templates/account/')

from . import views
