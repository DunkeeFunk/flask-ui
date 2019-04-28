from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager, current_user
import json
# local imports
from instance.config import app_config
from calls.weather import get_weather
from calls.ml_endpoint import get_ml_data

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):

    from uifactory.models import Users, Measurements, Plants, Models
    from .forms import RegistrationForm, LoginForm, AddPlantForm

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
        # get this users plants
        plants = Plants.query.filter_by(owner_id=current_user.public_id).all()
        # empty list to add each users current measurement
        users_measurements = []
        # this returns a dict with weather for the area
        weather = get_weather()
        # empty list for each plants predictions
        ml_results = []
        for plant in plants:
            # get that plants current measurement
            users_mea = Measurements.query.filter(Measurements.username.like(plant.sensor_id))\
                                            .order_by(Measurements.date_created.desc()).first()
            # get machine learning predictions for these measurements
            try:
                cur_ml = get_ml_data(str(users_mea.temp), str(users_mea.humidity), str(users_mea.light))
            except:
                cur_ml = get_ml_data("0", "0", "0")
            # append to a list of dicts
            ml_results.append(cur_ml)
            # put this into a list of queries
            users_measurements.append(users_mea)

        # pass all this out to the html template - needs formatted
        return render_template('home.html', title='Home', plants=zip(plants, users_measurements, ml_results), weather=weather)

    @ui.route('/addplant', methods=['GET', 'POST'])
    @login_required
    def add_plant():
        form = AddPlantForm()
        if form.validate_on_submit():
            # add plant to the db
            new_plant = Plants(plant_name=form.pl_name.data, plant_type=form.pl_type.data,
                               sensor_id=form.sen_id.data, public_id=current_user.public_id)
            # save plant in the db
            new_plant.save()
            return redirect(url_for('home'))
        return render_template('add_plant.html', title='Add Plant', form=form)

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
