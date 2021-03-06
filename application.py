from flask import send_from_directory

import api.settings
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api.api import rest_api

# Beanstalk looks for "application" variable
application = Flask(__name__)

file_blueprint = Blueprint('static_files', __name__, url_prefix='/site')


@file_blueprint.route('/<path:path>')
def files(path):
    return send_from_directory('static/dist', path)


@application.route('/')
def empty_route():  # Set default route
    return send_from_directory('static/dist', "index.html")


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = api.settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = api.settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = api.settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = api.settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = api.settings.RESTPLUS_ERROR_404_HELP


configure_app(application)
blueprint = Blueprint('api', __name__, url_prefix='/api')
rest_api.init_app(blueprint)
CORS(blueprint, resources={r"/api/*": {"origins": "*"}})
application.register_blueprint(file_blueprint)
application.register_blueprint(blueprint)


# Locally Relevant. Beanstalk has other notions...
def main():
    application.run(debug=api.settings.FLASK_DEBUG, port=80)


if __name__ == "__main__":
    main()
