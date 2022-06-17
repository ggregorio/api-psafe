"""
Creates the app, import its routes,
configure logging, and initialize the DB
"""

import logging

from flask import Flask

app = Flask(__name__)

from app import routes

logging.getLogger('werkzeug') \
    .addFilter(lambda record: 'GET /healthcheck' not in record.getMessage())
