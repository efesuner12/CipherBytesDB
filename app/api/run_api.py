from flask import Flask
from flask_restful import Api
from werkzeug.serving import run_simple

import ssl

from app.api.common.config import DevelopmentConfig
from app.api.common.routes import initialise_routes

## Creates the flask object, import the configurations and
# initialises the URLs and runs the server
def run():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    api = Api(app)

    initialise_routes(api)

    host, port = app.config['SERVER_NAME'].split(':')
    debug_enabled = app.config['DEBUG']

    # Comment below 2 lines if issues with SSL
    ssl_context = ssl.SSLContext(app.config['SSL_TLS_VERSION'])
    ssl_context.load_cert_chain(app.config['SSL_CERTIFICATE'], app.config['SSL_PRIVATE_KEY'])

    # Comment below line and uncomment the bottom line if issues with SSL
    run_simple(host, int(port), app, use_debugger=debug_enabled, ssl_context=ssl_context)
    #run_simple(host, int(port), app, use_debugger=debug_enabled)
