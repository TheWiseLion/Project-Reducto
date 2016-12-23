from flask import send_from_directory

import settings
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api import api

import logging.config


# Requirments: sumy 0.5.1, flask, flask restplus,

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

file_blueprint = Blueprint('static_files',__name__,
                           url_prefix='/site')
@file_blueprint.route('/<path:path>')
def files(path):
    print path
    return send_from_directory('../static/dist', path)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    CORS(blueprint, resources={r"/api/*": {"origins": "*"}})
    flask_app.register_blueprint(blueprint)
    flask_app.register_blueprint(file_blueprint)




def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    print app.url_map
    app.run(debug=settings.FLASK_DEBUG)



if __name__ == "__main__":
    main()