from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager, current_user
# local imports
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):

    from uifactory.models import Users, Measurements, Plants, Models
    from .forms import RegistrationForm, LoginForm

    ui = Flask(__name__, instance_relative_config=True)
    ui.config.from_object(app_config[config_name])
    ui.config.from_pyfile('config.py')
    ui.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(ui)
    login_manager = LoginManager(ui)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @ui.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.get_user_by_user_name(username=form.email.data)
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Try again', 'danger')
        return render_template('login.html', title='Login', form=form)

    @ui.route('/')
    @ui.route('/home')
    @login_required
    def home():
        # you will require this knowledge is 5 mins
        # we want to get the plants of the current user here
        # and pass them out through render template to be parsed by the html into panels
        print(type(current_user.public_id))
        # pass in the plants/panels here and render them
        return render_template('home.html', title='Home')

    @ui.route('/about')
    def about():
        return render_template('about.html', title='About')

    @ui.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            user = Users(user_name=form.email.data, public_id=str(uuid.uuid4()), password=hashed_password, admin=False)
            user.save()  # save to db
            flash(f'Your Account has been created for {form.email.data}!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @ui.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    return ui
