from flask import Flask

app = Flask(__name__)
# dashboard.bind(app)

from app import api