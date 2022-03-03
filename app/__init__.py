# encoding: utf-8
"""
Example RESTful API Server.
"""
from flask import Flask
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

def create_app(**kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """

    # Initialize the Flas-App
    app: Flask = Flask(__name__, **kwargs)

    # Load the config file
    app.config.from_object('config.DevelopmentConfig')

    # Initialize the API extensions
    from . import extensions
    extensions.init_app(app)

    # Initialize the actual API routes
    from . import modules
    modules.init_app(app)

    return app
