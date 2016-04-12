#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

account_blueprint = Blueprint('account', __name__, template_folder='../templates/account/')


def index_rank(index):
    return int(index) + 1

account_blueprint.add_app_template_filter(index_rank, 'torank')


from . import views
