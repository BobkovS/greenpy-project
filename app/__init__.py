import logging

from flask import Flask

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    app.logger.setLevel(logging.INFO)

    app.logger.info('GreenPy startup')

    return app
