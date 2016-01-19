#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string

from flask import render_template, request, session, redirect, url_for, send_from_directory
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from models import *
from . import prob_blueprint
from .. import db
from werkzeug.exceptions import BadRequestKeyError


def randomkey(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


@prob_blueprint.route('/list')
def list():
    from ..account.models import User
    all_user = db.session.query(User).filter_by(active=True).order_by(desc('score')).all()
    for user in all_user:
        if len(user.prob) == 0:
            all_user.pop(all_user.index(user))
        else:
            for i in user.prob:
                if not i.active:
                    user.prob.pop(user.prob.index(i))

    try:
        if session['login'] is True:
            u = db.session.query(User).filter_by(userid=session['userid']).first()
            success_prob = u.success_prob
        else:
            success_prob = []
    except KeyError:
        session['login'] = False
        success_prob = []

    return render_template('prob.html',
                           user_data=all_user,
                           success=success_prob)


def addfile(f, p):
    if f.filename == '':
        if p.file is None:
            return "default.png"
        else:
            return p.file
    else:
        filetype = '.' + f.filename.split('.')[-1]
        filename = randomkey(len(f.filename)) + filetype
        f.save(prob_blueprint.root_path + '/prob_images/' + filename)
        return filename


@prob_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    from ..account.models import User

    try:
        if session['login'] is not True:
            return redirect(url_for('account.login'))
    except KeyError:
        return redirect(url_for('account.login'))

    if request.method == 'GET':
        error = False
        try:
            if request.args['error'] == 'authkey':
                error = True
        except BadRequestKeyError:
            pass

        prob_list = db.session.query(Prob).filter_by(maker_nick=session['nickname']).all()
        return render_template('upload.html',
                               prob_list=prob_list,
                               keyerror=error)
    else:
        data = request.form
        for i in data:
            if i == 'probimage':
                continue
            elif data[i] == '':
                return redirect(url_for('.upload'))
        if data['onoff'] == 'on':
            onoff = True
        elif data['onoff'] == 'off':
            onoff = False
        f = request.files['probimage']

        p = db.session.query(Prob).filter_by(id=data['id']).first()

        if p is None or data['add'] == 'true':
            u = db.session.query(User).filter_by(userid=session['userid'], nickname=session['nickname']).first()
            p = Prob()
            p.title = data['probtitle']
            p.score = data['probscore']
            p.key = data['probkey']
            p.content = data['probcontent']
            p.maker_id = u.id
            p.maker_nick = u.nickname
            p.maker = u
            p.file = addfile(f, p)
            p.active = onoff

            db.session.add(p)

        else:
            p.title = data['probtitle']
            p.score = data['probscore']
            if p.key != data['probkey']:
                p.key = data['probkey']
            p.content = data['probcontent']
            p.file = addfile(f, p)
            p.active = onoff
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('.upload', error='authkey')+'#ProbTitle')

        return redirect(url_for('.upload'))


@prob_blueprint.route('/prob_image/<path:filename>')
def prob_image(filename):
    return send_from_directory(prob_blueprint.root_path + '/prob_images/', filename)


@prob_blueprint.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html',
                               error=None)
    else:
        key = request.form['authkey']
        p = db.session.query(Prob).filter_by(key=key).first()
        if p is None:
            return render_template('auth.html',
                                   error='true')
        else:
            from ..account.models import User
            u = db.session.query(User).filter_by(userid=session['userid']).first()
            if p in u.success_prob:
                return render_template('auth.html',
                                       error='dup')
            u.success_prob.append(p)
            u.score = (int(u.score) + int(p.score))
            return render_template('auth.html',
                                   error='false',
                                   title=p.title)


@prob_blueprint.route('/dupcheck')
def dupcheck():
    key = request.args['key']
    if db.session.query(Prob).filter_by(key=key).first() is not None:
        return 'true'
    else:
        return 'false'
