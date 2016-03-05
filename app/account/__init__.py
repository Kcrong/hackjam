#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, session, redirect, request
from time import time
from werkzeug.exceptions import BadRequestKeyError

account_blueprint = Blueprint('account', __name__, template_folder='../templates/account/')

"""
@account_blueprint.before_request
def account_before_request():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            session_time = session['time']
        except KeyError:
            session_time = session['time'] = str(time())
        try:
            request_time = request.args['time']
        except BadRequestKeyError:
            session['time'] = str(time())
            if len(request.args) != 0:
                return redirect(request.url + '&time=' + session['time'])
            else:
                return redirect(request.url + '?time=' + session['time'])

        if session_time != request_time:
            session['time'] = str(time())

            if len(request.args) != 0:
                redirect_url = request.url + '&time=' + session['time']
            else:
                redirect_url = request.url + '?time=' + session['time']
            session['time'] = 0
            return redirect(redirect_url)
"""

from . import views
