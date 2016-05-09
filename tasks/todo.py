# -*- coding: utf-8 -*-
from celery import Celery
from celery.contrib.methods import task_method
import celeryconfig

celery = Celery('TodoTask')
celery.config_from_object(celeryconfig)


class TodoTask(object):
    def __init__(self):
        pass

    @celery.task(filter=task_method, name='TodoTask.run')
    def run(self, task_data):
        return 'task {0}'.format(task_data)

    @celery.task(filter=task_method, name='TodoTask.create')
    def create(self, obj_cls, **kwargs):
        todo = obj_cls.objects.create(**kwargs)

        return todo.title
