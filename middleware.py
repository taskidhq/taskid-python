from werkzeug.wrappers import Request, Response, ResponseStream
import re
from get_emails import GetEmails
from taskid import Taskid
import json
from taskid_json_encoder import TaskidJSONEncoder

class taskid_middleware():
    '''
    Simple Taskid WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        match = taskid_middleware.match_task_url(request.path)

        print(request.path)
        if request.method == "GET" and re.match(r'\/tasks\/?$', request.path):
            return taskid_middleware.get_tasks(environ, start_response)
        elif request.method == "GET" and match:
            task_id = match.group(1)
            return taskid_middleware.get_task(task_id, environ, start_response)
        elif request.method == "POST" and match:
            task_id = match.group(1)
            body = json.loads(request.get_data())
            return taskid_middleware.run_task(task_id, body, environ, start_response)
        else:
            return self.app(environ, start_response)

    @staticmethod
    def get_tasks(environ, start_response):
        json_response = json.dumps(Taskid.get_tasks())
        res = Response(json_response, mimetype= 'application/json', status=200)

        return res(environ, start_response)

    @staticmethod
    def get_task(task_id, environ, start_response):
        json_response = json.dumps(Taskid.get_task(task_id), cls=TaskidJSONEncoder)
        res = Response(json_response, mimetype= 'application/json', status=200)

        return res(environ, start_response)

    @staticmethod
    def run_task(task_id, body, environ, start_response):
        result = Taskid.run_task(task_id, body)
        json_response = json.dumps(result)
        res = Response(json_response, mimetype= 'application/json', status=200)

        return res(environ, start_response)

    @staticmethod
    def match_task_url(path):
        return re.search(r'\/tasks\/(\w+)\/?', path)
