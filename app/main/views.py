#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, redirect, url_for, session

from . import main_blueprint
from .. import app


@main_blueprint.route('/')
def main_index():
    return redirect(url_for('main.index'))


@main_blueprint.route('/index')
def index():
    return render_template('index.html')


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


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path + '/static/', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main_blueprint.route('/prob_image/<path:filename>')
def prob_image(filename):
    return send_from_directory(main_blueprint.root_path + '/../prob/prob_images/', filename)


@main_blueprint.route('/upload_files/<path:filename>')
def prob_file(filename):
    return send_from_directory(main_blueprint.root_path + '/../prob/prob_files/', filename)