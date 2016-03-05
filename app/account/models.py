#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .. import db
from ..prob.models import Prob
from datetime import datetime

success_probs = db.Table('success_probs',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('prob_id', db.Integer, db.ForeignKey('prob.id'))
                         )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    userid = db.Column(db.String(30), unique=True, nullable=False)
    userpw = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    nickname = db.Column(db.String(30), unique=True, nullable=False)
    is_admin = db.Column(db.BOOLEAN, default=False, nullable=False)
    prob = db.relationship(Prob)
    success_prob = db.relationship('Prob', secondary=success_probs,
                                   backref=db.backref('users'))
    created = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    updated = db.Column(db.DATETIME, default=datetime.now(), nullable=False, onupdate=datetime.now())


