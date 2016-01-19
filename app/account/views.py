#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, session
from .. import db
from . import account_blueprint
from .models import User
from werkzeug.exceptions import BadRequestKeyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc


@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            error = request.args.get('error')
        except BadRequestKeyError:
            pass
        else:
            if error == "userid":
                return render_template('login.html',
                                       iderror=u"사용할 수 없는 아이디 입니다.")
            elif error == "nickname":
                return render_template('login.html',
                                       nickerror=u"사용할 수 없는 닉네임 입니다.")
            else:
                pass

        return render_template('login.html')

    else:
        data = request.form
        u = db.session.query(User).filter_by(userid=data['userid'], userpw=data['userpw'], active=True).first()
        if u is not None:
            session['login'] = True
            session['userid'] = u.userid
            session['nickname'] = u.nickname
            session['admin'] = u.is_admin
            return redirect(url_for('main.main_index'))
        else:
            return render_template('login.html',
                                   loginerror=True)


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
    from ..prob.models import Prob
    # userid
    # userpw
    # nickname
    u = User()
    u.userid = request.form['userid']
    u.userpw = request.form['userpw']
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
        return redirect(url_for('account.login'))


@account_blueprint.route('/logout')
def logout():
    session['login'] = False
    session['nickname'] = 'Guest'
    session['userid'] = 'Guest'
    session['admin'] = False
    return redirect(url_for('.login'))


@account_blueprint.route('/rank')
def rank():
    rank = db.session.query(User).filter_by(active=True).order_by(desc('score')).all()
    return render_template('rank.html',
                           rank=rank,
                           rank_cnt=len(rank))
