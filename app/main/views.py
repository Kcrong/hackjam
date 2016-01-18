#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, redirect, url_for

from . import main_blueprint
from .. import app


@main_blueprint.route('/')
def main_index():
    return redirect(url_for('main.index'))


@main_blueprint.route('/index')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/auth')
def blog():
    return render_template('main/auth.html')


@main_blueprint.route('/rank')
def contact():
    return render_template('main/rank.html')


@main_blueprint.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@main_blueprint.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@main_blueprint.route('/img/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/static/img/', filename)


@main_blueprint.route('/fonts/<path:filename>')
def font_static(filename):
    return send_from_directory(app.root_path + '/static/fonts/', filename)
