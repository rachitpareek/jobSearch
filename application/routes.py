from application import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from application.forms import LoginForm, RegistrationForm, EditProfileForm, ApplicationForm
from application.models import User, Application
from datetime import datetime, timedelta

def clean_date(date):
    date = date - timedelta(hours=8, minutes=0)
    return date.strftime("%d %B, %Y") + " at " + date.strftime("%-I:%-M %p")

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    apps = current_user.positions_applied_to().paginate(
        page, app.config['APPS_PER_PAGE'], False)
    next_url = url_for('dashboard', page=apps.next_num) if apps.has_next else None
    prev_url = url_for('dashboard', page=apps.prev_num) if apps.has_prev else None
    return render_template('dashboard.html', title='Home',
                           apps=apps.items, next_url=next_url,
                           prev_url=prev_url, clean_date=clean_date)

@app.route('/tracking', methods=['GET', 'POST'])
@login_required
def tracking():
    form = ApplicationForm()
    if form.validate_on_submit():
        input_app = Application(company=form.company.data.strip(), position=form.position.data.strip(), status=form.status.data, applier=current_user)
        db.session.add(input_app)
        db.session.commit()
        flash('You have inputted a new application for a role at' + form.company.data.strip() + '!')
        return redirect(url_for('tracking'))
    return render_template("tracking.html", title='Tracking', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/application/<app_id>')
@login_required
def application(app_id):
    app = Application.query.filter_by(id=app_id).first_or_404()
    return render_template('application.html', app=app, clean_date=clean_date)

@app.route('/analytics')
@login_required
def analytics():
    page = request.args.get('page', 1, type=int)
    apps = current_user.positions_applied_to().paginate(
        page, app.config['APPS_PER_PAGE'], False)
    companies = set([app.company for app in apps.items])
    print(companies)
    next_url = url_for('dashboard', page=apps.next_num) if apps.has_next else None
    prev_url = url_for('dashboard', page=apps.prev_num) if apps.has_prev else None
    return render_template('analytics.html', title='Home', user=current_user,
                           apps=apps.items, companies=companies)
