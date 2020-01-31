from app import app
import os


import json
import logging
import pandas as pd
import traceback


from flask import Flask, request, make_response, jsonify
from flask_restplus import Resource, Api, reqparse, fields
from logging.handlers import RotatingFileHandler
from time import strftime
from werkzeug.middleware.proxy_fix import ProxyFix
import flask_monitoringdashboard as dashboard

# app = Flask(__name__)
dashboard.bind(app)
api = Api(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

handler = RotatingFileHandler('app.log', backupCount=10)
# getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
# getLogger('werkzeug'): decorators loggers to file + nothing to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)
logger.addHandler(handler)

# @app.route("/")
# def index():
#
#     # Use os.getenv("key") to get environment variables
#     app_name = os.getenv("APP_NAME")
#
#     if app_name:
#         return f"Hello from {app_name} running in a Docker container behind Nginx!"
#
#     return "Hello from Flask"

# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args()

ns_hello = api.namespace('hello', description='hello')



hello = ns_hello.model("Hello",
                  {
                     "name": fields.String(
                         description="Name",
                         example="Alex", required=True)
                  })


@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        print('{} {}\n{} {} {} {}\nRequest Data: {}\n{}'.format(
                     'New Request Logged at:',
                     ts,
                     request.scheme,
                     request.method,
                     request.remote_addr,
                     request.full_path,
                     request.data,
                     response.status))
        logger.error('%s %s %s %s %s %s %s',
                     ts,
                     request.scheme,
                     request.method,
                     request.remote_addr,
                     request.full_path,
                     request.data,
                     response.status)
    return response

@ns_hello.route('/')
class HELLO(Resource):
    def get(self):
        return make_response({"message": "hello"})

    @ns_hello.doc("hello world", body=hello, responses={200: 'Success', 400: 'Validation Error'})
    def post(self):
        data = json.loads(request.data)
        name = data.get('name')
        print(name)
        hello_msg = "hello {}".format(name)
        return make_response({"message": hello_msg})


@api.errorhandler(Exception)
def handle_all_exception(error):
    # print('error', error)
    if type(error) == type(KeyError()):
        message = 'There may not be enough data to perform NER'
    else:
        message = 'Unknown {} Error'.format(type(error))

    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    print('hello')
    error_str = '%s %s %s %s %s Request Data: %s %s 400 DATA VALIDATION ERROR\n%s' % (
                ts,
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                request.data,
                message,
                tb)
    print('STRING', error_str)
    logger.error('%s %s %s %s %s Request Data: %s %s 500 INTERNAL SERVER ERROR\n%s',
                 ts,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 request.data,
                 message,
                 tb)

    return {'message': message}, 400