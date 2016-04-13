#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError, RequestEntityTooLarge

from . import prob_blueprint
from ..models import *


@prob_blueprint.route('/list')
def list():
    all_category = Category.query.filter_by(active=True).all()

    return render_template('prob/prob.html',
                           category_data=all_category,
                           success=current_user.success_prob)


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
            return redirect(url_for('.upload', error='첨부파일이 너무 큽니다!'))

        # post 요청 데이터 점검
        for i in data:
            if not i in ['probimage', 'probfile'] and len(data[i]) == 0:
                return redirect(url_for('.upload', error='제목, 카테고리, 인증키, 내용을 모두 입력해주세요!'))

        _onoff = {
            'on': True,
            'off': False
        }

        p = db.session.query(Prob).filter_by(id=data['id']).first()
        u = current_user
        c = db.session.query(Category).filter_by(title=data['category']).first()

        if data['add'] == 'true' or p is None:
            p = Prob()
            db.session.add(p)

        valid_files = [(request.files[req_filename], req_filename)  # request.files[req_filename], req_filename 리스트
                       for req_filename in request.files  # 받은 파일 리스트 중,
                       if len(request.files[req_filename].filename) > 0]  # 해당 이름을 가진 파일의 이름 길이가 0이 아닐때만 리스트에 포함

        for file, filename in valid_files:  # 유효한 파일들 중에서
            p.savefile(file, filename)  # 저장

        p.title = data['probtitle']

        if p.key != data['probkey']:
            p.key = data['probkey']

        p.content = data['probcontent']

        p.active = _onoff[data['onoff']]
        p.maker = u
        p.category = c

        try:
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            return redirect(url_for('.upload', error='사용할 수 없는 인증키 입니다!') + '#ProbTitle')

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
    if Prob.query.filter_by(key=key).first() is not None:
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
        if current_user.is_authenticated is False:
            return redirect(url_for('account.login'))

        else:  # 로그인한 사용자만
            content = request.form['talk']

            db.session.add(Talk(content, current_user))
            db.session.commit()

            return redirect(url_for('prob.talking'))
