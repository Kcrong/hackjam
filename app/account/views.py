#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError

from . import account_blueprint
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

        u = User.query.filter_by(userid=data['userid'], userpw=hash(data['userpw']), active=True).first()

        if u is None:
            return render_template('account/login.html',
                                   alert_message=['아이디 혹은 비밀번호가 잘못 입력되었습니다.'])

        else:
            session['login'] = True
            session['userid'] = u.userid
            session['id'] = u.id
            session['admin'] = u.is_admin
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
    if len(request.form['userid']) < 6:
        return redirect(url_for('account.login', error="userid"))
    elif len(request.form['nickname']) < 6:
        return redirect(url_for('account.login', error="nickname"))

    u = User()
    u.userid = request.form['userid']
    u.userpw = hash(request.form['userpw'])
    u.nickname = request.form['nickname']

    u.success_prob.append(Prob.query.filter_by(title="signup").first())
    db.session.add(u)
    try:
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        dupkey = e.args[0].split('for key')[1].split("'")[1]
        return redirect(url_for('account.login', error=dupkey))
    else:
        return redirect(url_for('account.login', error='None'))


@account_blueprint.route('/logout')
def logout():
    session['login'] = False
    session['nickname'] = 'Guest'
    session['userid'] = 'Guest'
    session['admin'] = False
    return redirect(url_for('.login'))


@account_blueprint.route('/rank')
def rank():
    rank = User.query.filter_by(active=True).order_by(desc('score'), 'updated').all()
    return render_template('account/rank.html',
                           rank=rank)
