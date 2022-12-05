from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    from app.config import BaseConfig
    app.config.from_object(BaseConfig)
    from app.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        from app.blueprints import api
        app.register_blueprint(api)
        # app.register_blueprint(api, url_prefix='/api')
    return app
