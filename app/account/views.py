#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequestKeyError

from . import account_blueprint
from ..models import *


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            error = request.args.get('error')
        except BadRequestKeyError:
            pass
        else:
            if error == "userid":
                return render_template('account/login.html',
                                       useradd_error=True,
                                       useradd_error_message=u"사용할 수 없는 아이디 입니다.")
            elif error == "nickname":
                return render_template('account/login.html',
                                       useradd_error=True,
                                       useradd_error_message=u"사용할 수 없는 닉네임 입니다.")
            elif error == 'None':
                return render_template('account/login.html',
                                       success=True)
            else:
                pass

        return render_template('account/login.html')

    else:
        data = request.form

        try:

            u = db.session.query(User).filter_by(userid=data['userid'], userpw=hash(data['userpw']), active=True).one()

        except NoResultFound:
            return render_template('account/login.html',
                                   loginerror=True)
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
        userid = request.args['id']
    except BadRequestKeyError:
        # nick dup check
        if db.session.query(User).filter_by(nickname=request.args['nick']).first() is not None:

            return "true"
        else:

            return "false"

    else:
        # id dup check
        if db.session.query(User).filter_by(nickname=userid).first() is not None:

            return "true"
        else:

            return "false"


@account_blueprint.route('/useradd', methods=['POST'])
def useradd():
    # userid
    # userpw
    # nickname

    if len(request.form['userid']) < 6:
        return redirect(url_for('account.login', error="userid"))
    elif len(request.form['nickname']) < 6:
        return redirect(url_for('account.login', error="nickname"))

    u = User()
    u.userid = request.form['userid']
    u.userpw = hash(request.form['userpw'])
    u.nickname = request.form['nickname']

    u.success_prob.append(db.session.query(Prob).filter_by(title="signup").first())
    db.session.add(u)
    try:
        db.session.commit()

    except IntegrityError, e:
        db.session.rollback()
        dupkey = e[0].split('for key')[1].split("'")[1]
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


def test(tmp):
    for i in tmp:
        print i.score, i.updated


@account_blueprint.route('/rank')
def rank():
    rank = User.query.filter_by(active=True).order_by(desc('score'), 'updated').all()
    return render_template('rank.html',
                           rank=rank,
                           rank_cnt=len(rank))
