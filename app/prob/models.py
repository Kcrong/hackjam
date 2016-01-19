#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .. import db


class Prob(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(1000))
    key = db.Column(db.String(30), nullable=False, unique=True)
    maker_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    maker_nick = db.Column(db.String(50))
    maker = db.relationship('User',
                            backref=db.backref('probes', lazy='dynamic'))
    active = db.Column(db.BOOLEAN, default=True, nullable=False)
    file = db.Column(db.String(50))

