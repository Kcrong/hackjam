#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .. import db


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
