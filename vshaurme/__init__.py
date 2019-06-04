import os
from datetime import datetime

import click
from flask import Flask, render_template, g, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
from dotenv import load_dotenv

from vshaurme.blueprints.admin import admin_bp
from vshaurme.blueprints.ajax import ajax_bp
from vshaurme.blueprints.auth import auth_bp
from vshaurme.blueprints.main import main_bp
from vshaurme.blueprints.user import user_bp
from vshaurme.blueprints.api import api_bp
from vshaurme.blueprints.vk_auth import vkoauth_bp

from vshaurme.extensions import bootstrap, db, login_manager, mail, dropzone, moment, whooshee, avatars, csrf, babel, oauth
from vshaurme.models import Role, User, Photo, Tag, Follow, Notification, Comment, Collect, Permission
from vshaurme.settings import config
from vshaurme.bad_words import init_badwords_files
from vshaurme.utils import export_users_to_csv


def create_app(config_name=None):
    load_dotenv()

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask('vshaurme')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)
    register_locale_language(app)
    register_rollbar(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    avatars.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)
    oauth.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(vkoauth_bp, url_prefix='/vk')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Photo=Photo, Tag=Tag,
                    Follow=Follow, Collect=Collect, Comment=Comment,
                    Notification=Notification)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            notification_count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
        else:
            notification_count = None
        return dict(notification_count=notification_count)


def register_rollbar(app):
    @app.before_first_request
    def init_rollbar():
        rollbar.init(os.getenv('ROLLBAR_TOKEN'),
                     root=os.path.dirname(os.path.realpath(__file__)),
                     allow_logging_basic_config=False
                     )
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


def register_locale_language(app):
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    @app.before_request
    def add_locale_in_g():
        g.locale = get_locale()


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def init():
        """Initialize Vshaurme."""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    @click.option('--follow', default=30, help='Quantity of follows, default is 30.')
    @click.option('--photo', default=30, help='Quantity of photos, default is 30.')
    @click.option('--tag', default=20, help='Quantity of tags, default is 20.')
    @click.option('--collect', default=50, help='Quantity of collects, default is 50.')
    @click.option('--comment', default=100, help='Quantity of comments, default is 100.')
    def forge(user, follow, photo, tag, collect, comment):
        """Generate fake data."""

        from vshaurme.fakes import fake_admin, fake_comment, fake_follow, fake_photo, fake_tag, fake_user, fake_collect

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('Generating %d follows...' % follow)
        fake_follow(follow)
        click.echo('Generating %d tags...' % tag)
        fake_tag(tag)
        click.echo('Generating %d photos...' % photo)
        fake_photo(photo)
        click.echo('Generating %d collects...' % photo)
        fake_collect(collect)
        click.echo('Generating %d comments...' % comment)
        fake_comment(comment)
        click.echo('Done.')

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('locale')
    def init(locale):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d vshaurme/translations -l ' + locale):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d vshaurme/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d vshaurme/translations'):
            raise RuntimeError('compile command failed')

    @app.cli.command()
    def getbadwords():
        """Downloading Bad Words."""
        click.echo('Downloading bad words...')
        click.echo(init_badwords_files())
        click.echo('Done.')

    @app.cli.command()
    @click.option('--path', default=app.config['VSHAURME_UPLOAD_PATH'])
    @click.option('--filename', default="users.csv")
    def getuseremails(path, filename):
        """Export User Emails to csv file."""
        filepath = os.path.join(path, filename)
        click.echo(f'Exporting to {filepath}...')
        click.echo(f'{export_users_to_csv(filepath)} users exported')
        click.echo('Done.')