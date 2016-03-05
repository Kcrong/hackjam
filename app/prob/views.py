#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string

from flask import render_template, request, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError, RequestEntityTooLarge
from datetime import datetime

from models import *
from . import prob_blueprint
from .. import db


def randomkey(length):
    result = ''.join(random.choice(string.lowercase) for i in range(length))
    return result[:3000]


@prob_blueprint.route('/list')
def list():
    from ..account.models import User

    all_category = db.session.query(Category).filter_by(active=True).all()

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
                           category_data=all_category,
                           success=success_prob)


def saveimagefile(getfile, p):
    if getfile.filename == '':
        if p.image is None:
            p.image = 'default.png'
            p.image_original = 'default.png'

    else:
        p.image_original = getfile.filename
        filename = randomkey(len(getfile.filename)) + '.' + getfile.filename.split('.')[-1]
        getfile.save(prob_blueprint.root_path + '/prob_images/' + filename)
        p.image = filename


def saveprobfile(getfile, p):
    if getfile.filename == '':
        if p.file is None:
            p.file = ''
            p.file_original = ''

    else:
        p.file_original = getfile.filename
        filename = randomkey(len(getfile.filename)) + '.' + getfile.filename.split('.')[-1]
        getfile.save(prob_blueprint.root_path + '/prob_files/' + filename)
        p.file = filename


@prob_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    from ..account.models import User

    try:
        if session['login'] is not True:
            return redirect(url_for('account.login'))
    except KeyError:
        return redirect(url_for('account.login'))

    if request.method == 'GET':
        try:
            error = request.args['error']
        except BadRequestKeyError:
            error = False

        prob_list = db.session.query(Prob).filter_by(maker_id=session['id']).all()
        category_list = db.session.query(Category).filter_by(active=True).all()

        return render_template('upload.html',
                               category_list=category_list,
                               prob_list=prob_list,
                               error=error)
    else:
        try:
            data = request.form
        except RequestEntityTooLarge:
            return redirect(url_for('.upload', error='bigfile'))
        for i in data:
            if i == 'probimage' or i == 'probfile':
                continue
            elif data[i] == '':
                return redirect(url_for('.upload', error='nodata'))

        if data['onoff'] == 'on':
            onoff = True
        elif data['onoff'] == 'off':
            onoff = False
        probimage = request.files['probimage']
        probfile = request.files['probfile']
        p = db.session.query(Prob).filter_by(id=data['id']).first()
        u = db.session.query(User).filter_by(id=session['id']).first()
        c = db.session.query(Category).filter_by(title=data['category']).first()

        if p is None or data['add'] == 'true':
            p = Prob()
            db.session.add(p)

        p.title = data['probtitle']
        if p.key != data['probkey']:
            p.key = data['probkey']
        p.content = data['probcontent']
        p.maker_id = u.id
        saveimagefile(probimage, p)
        saveprobfile(probfile, p)
        p.active = onoff
        p.maker = u
        p.maker_id = u.id
        p.category_id = c.id
        p.category = c

        try:
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            return redirect(url_for('.upload', error='authkey') + '#ProbTitle')

        return redirect(url_for('.upload'))


@prob_blueprint.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html',
                               error=None)
    else:
        try:
            if not session['login']:
                return render_template('auth.html',
                                       error='login')
        except KeyError:
            return redirect(url_for('account.login'))
        from ..account.models import User

        key = request.form['authkey']
        p = db.session.query(Prob).filter_by(key=key).first()
        u = db.session.query(User).filter_by(userid=session['userid']).first()

        if p is None:
            return render_template('auth.html',
                                   error='true')
        elif p.maker_id == u.id:
            return render_template('auth.html',
                                   error='mine')
        else:
            if p in u.success_prob:
                return render_template('auth.html',
                                       error='dup')

            u.success_prob.append(p)
            u.score = int(u.score) + 1
            u.updated = datetime.now()
            db.session.commit()

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
