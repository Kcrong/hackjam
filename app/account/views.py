#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for
from flask.ext.login import login_user, logout_user
from flask.ext.security import login_required
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError

from . import account_blueprint
from .. import user_datastore
from ..models import *

user_error_message = {
    'userid': '사용할 수 없는 아이디 입니다.',
    'nickname': '사용할 수 없는 닉네임 입니다.',
    'None': '회원가입이 완료되었습니다.',
}


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            error = request.args.get('error')
            return render_template('account/login.html', alert_message=[user_error_message[error]])
        except (BadRequestKeyError, KeyError):
            pass

        return render_template('account/login.html')

    # request.method == 'POST'
    else:
        data = request.form

        u = User.query.filter_by(userid=data['userid'], userpw=data['userpw'], active=True).first()

        if u is None:
            return render_template('account/login.html',
                                   alert_message=['아이디 혹은 비밀번호가 잘못 입력되었습니다.'])

        else:
            login_user(u)
            return redirect(url_for('main.main_index'))


@account_blueprint.route('/dupcheck', methods=['GET'])
def dupcheck():
    # id or nick
    # return str(request.args)

    try:
        dup_check = User.query.filter_by(userid=request.args['id']).first()

    except BadRequestKeyError:
        dup_check = User.query.filter_by(nickname=request.args['nick']).first()

    if dup_check is None:
        return 'false'
    else:
        return 'true'


@account_blueprint.route('/useradd', methods=['POST'])
def useradd():
    data = request.form

    for req_name in ['userid', 'nickname']:
        if len(data[req_name]) < 6:
            return redirect(url_for('account.login', error=req_name))

    user_datastore.create_user(userid=data['userid'],
                               userpw=data['userpw'],
                               nickname=data['nickname'])

    try:
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        dupkey = e.args[0].split('for key')[1].split("'")[1]
        return redirect(url_for('account.login', error=dupkey))
    else:
        return redirect(url_for('account.login', error='None'))


@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@account_blueprint.route('/rank')
def rank():
    rank = User.query.filter_by(active=True).order_by(desc('score'), 'updated').all()
    return render_template('account/rank.html',
                           rank=rank)
