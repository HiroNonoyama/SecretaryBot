# -*- coding: utf-8 -*-
import datetime
from app import db


class Todo(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    detail = db.StringField(max_length=1000)
    deadline = db.DateTimeField()

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ['-created_at', 'deadline']
    }
