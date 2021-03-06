#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, redirect, url_for

from . import main_blueprint


@main_blueprint.route('/')
def main_index():
    return redirect(url_for('main.index'))


@main_blueprint.route('/index')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/whoami')
def aboutme():
    return render_template('main/about_admin.html')


@main_blueprint.route('/prob_image/<path:filename>')
def prob_image(filename):
    return send_from_directory(main_blueprint.root_path + '/../prob/prob_images/', filename)


@main_blueprint.route('/upload_files/<path:filename>')
def prob_file(filename):
    return send_from_directory(main_blueprint.root_path + '/../prob/prob_files/', filename)
