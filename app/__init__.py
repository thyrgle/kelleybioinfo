import os
from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('main/main.html')

    # Initialize database.
    from . import db
    db.init_app(app)

    # Initialize authentication blueprint.
    from . import auth
    app.register_blueprint(auth.bp)

    # Initialize user profile.
    from . import profile
    app.register_blueprint(profile.bp)

    app.add_url_rule('/', endpoint='index')

    return app
