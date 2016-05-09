from flask import Blueprint, Response, request
from flask.views import MethodView
from models import Todo
from tasks.todo import TodoTask

todos = Blueprint('todos', __name__)


class ListView(MethodView):
    def get(self):
        todo = Todo.objects.first()
        task = TodoTask()
        task.create(obj_cls=Todo, title='this is mongo')
        return todo.title

todos.add_url_rule('/', view_func=ListView.as_view('list'))

