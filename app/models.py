# -*- coding:utf-8 -*-

from datetime import datetime
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.login import AnonymousUserMixin

from . import db

success_probs = db.Table('success_probs',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('prob_id', db.Integer, db.ForeignKey('prob.id'))
                         )

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.INTEGER, db.ForeignKey('user.id')),
                       db.Column('role_id', db.INTEGER, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
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

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User %s>" % self.nickname

    def __init__(self, **kwargs):
        self.success_prob.append(Prob.query.filter_by(title='signup').first())
        self.userid = kwargs.get('userid')
        self.userpw = kwargs.get('userpw')
        self.nickname = kwargs.get('nickname')


class AnonymousUser(AnonymousUserMixin):
    success_prob = list()
    is_admin = False
    nickname = "Guest"

    def __repr__(self):
        return "<Anonymous Guest>"


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

    def __repr__(self):
        return "<Prob %s>" % self.title


class Category(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(100))
    prob = db.relationship(Prob)
    active = db.Column(db.BOOLEAN, default=True)

    @property
    def probes(self):
        return db.object_session(self).query(Prob).filter_by(active=True).with_parent(self).all()

    def __repr__(self):
        return "<Category %s>" % self.title

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

    def __repr__(self):
        return "<Talk by %s>" % self.user.nickname
