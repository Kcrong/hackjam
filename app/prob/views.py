#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string

from flask import render_template, request, session, redirect, url_for
from flask.ext.security import current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError, RequestEntityTooLarge
from sqlalchemy import desc
from ..models import *
from . import prob_blueprint


def randomkey(length):
    result = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    return result[:3000]


@prob_blueprint.route('/list')
def list():
    all_category = Category.query.filter_by(active=True).all()

    return render_template('prob/prob.html',
                           category_data=all_category,
                           success=current_user.success_prob)


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
@login_required
def upload():
    if request.method == 'GET':
        try:
            error = request.args['error']
        except BadRequestKeyError:
            error = False

        category_list = Category.query.filter_by(active=True).all()

        return render_template('prob/upload.html',
                               category_list=category_list,
                               prob_list=current_user.prob,
                               error=error)
    # request.method == 'POST'
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
@login_required
def auth():
    if request.method == 'GET':
        return render_template('prob/auth.html',
                               error=None)
    else:

        p = Prob.query.filter_by(key=request.form['authkey'], active=True).first()
        title = None

        if p is None:  # 해당 인증키인 문제가 없을 경우
            error = '올바른 인증키가 아닙니다!'
        elif p in current_user.prob:  # 자신이 낸 문제일 경우
            error = '자신이 낸 문제는 인증할 수 없습니다!'
        elif p in current_user.success_prob:  # 이미 인증한 문제일 경우
            error = '이미 인증한 문제입니다.'
        else:
            current_user.success_prob.append(p)
            current_user.score = int(current_user.score) + 1
            db.session.commit()

            error = False
            title = p.title

        return render_template('prob/auth.html',
                               error=error,
                               title=title)


@prob_blueprint.route('/dupcheck')
def dupcheck():
    key = request.args['key']
    if db.session.query(Prob).filter_by(key=key).first() is not None:

        return 'true'
    else:

        return 'false'


@prob_blueprint.route('/talk', methods=['GET', 'POST'])
def talking():
    if request.method == 'GET':
        all_talk = Talk.query.filter_by(active=True).order_by(desc('id')).all()
        return render_template('prob/talk.html',
                               all_talk=all_talk)

    elif request.method == 'POST':
        if session['login'] is False:
            return redirect(url_for('account.login'))

        content = request.form['talk']
        user = User.query.filter_by(userid=session['userid']).first()

        db.session.add(Talk(content, user))
        db.session.commit()

        return redirect(url_for('prob.talking'))
