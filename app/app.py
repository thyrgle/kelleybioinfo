import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # TODO Avoid global
    app = Flask(__name__, instance_relative_config=True)
    csrf = CSRFProtect()
    # TODO Secret key?
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.secret_key = 'dev'
    csrf.init_app(app)

    from . import models
    with app.app_context():
        # TODO Should this be here?
        models.db.init_app(app)
        models.db.drop_all()
        models.db.create_all()

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('main/main.html')

    # Initialize authentication blueprint.
    from . import auth
    app.register_blueprint(auth.bp)

    # Initialize user profile.
    from . import profile
    app.register_blueprint(profile.bp)

    # Initialize problems.
    from . import problems
    problems.load_problems()
    app.register_blueprint(problems.bp)

    app.add_url_rule('/', endpoint='index')

    return app
