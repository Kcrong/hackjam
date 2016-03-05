# -*- coding:utf-8 -*-

from . import db
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
    prob = db.relationship('Prob')
    success_prob = db.relationship('Prob', secondary=success_probs,
                                   backref=db.backref('users'))
    created = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    updated = db.Column(db.DATETIME, default=datetime.now(), nullable=False, onupdate=datetime.now())


class Prob(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(1000))
    key = db.Column(db.String(30), nullable=False, unique=True)
    maker_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    maker = db.relationship('User',
                            backref=db.backref('probes'))
    active = db.Column(db.BOOLEAN, default=True, nullable=False)
    image = db.Column(db.String(3000))
    image_original = db.Column(db.String(300))
    file = db.Column(db.String(3000))
    file_original = db.Column(db.String(300))
    category = db.relationship('Category')
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.id'))


class Category(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(100))
    prob = db.relationship(Prob)
    active = db.Column(db.BOOLEAN, default=True)

    @property
    def probes(self):
        return db.object_session(self).query(Prob).filter_by(active=True).with_parent(self).all()


class Talk(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    content = db.Column(db.TEXT, nullable=False)
    user = db.relationship(User)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, nullable=False, default=True)
    added = db.Column(db.DATETIME, nullable=False, default=datetime.now())

    def __init__(self, content, user):
        self.content = content
        self.user = user