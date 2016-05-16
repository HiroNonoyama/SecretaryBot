from flask import Blueprint, Response, request
from flask.views import MethodView
from models import Todo
from tasks.record_handler import TodoTask

todos = Blueprint('todos', __name__)


class BotView(MethodView):
    def get(self):
        todo = Todo.objects.first()
        task = TodoTask()
        task.create(obj_cls=Todo, title='this is mongo')
        return todo.title

    def post(self):
        req = request.json
    	task = TodoTask()
    	task.call(Todo, req)

        return Response(status=200)

todos.add_url_rule('/', view_func=BotView.as_view('list'))