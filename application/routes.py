from application import app, db
from flask import render_template, flash, redirect, url_for, request, Markup
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import plotly.graph_objects as go
from plotly import offline as po
from application.forms import LoginForm, RegistrationForm, EditProfileForm, ApplicationForm, UpdateApplicationForm, DeleteApplicationForm
from application.models import User, Application
from datetime import datetime, timedelta
import os

def clean_date(date):
    date = date - timedelta(hours=8, minutes=0)
    return date.strftime("%d %B, %Y") + " at " + date.strftime("%-I:%-M %p")

def make_sankey():
    if current_user.is_anonymous:
        return ""
    apps = list(current_user.positions_applied_to())
    companies = set([app.company for app in apps])
    data = [len([app for app in apps if app.status == "Applied"]), 
            len([app for app in apps if app.status == "Interviewing"]),
            len([app for app in apps if app.status == "Offer"]),
            len([app for app in apps if app.status == "Rejected"])]
    no_response = sum(data) - (data[1] + data[2] + data[3])
    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 1),
        label = ["Applied: " + str(sum(data)), "Interviewing: "  + str(data[1] + data[2]), 
                "Offer: " + str(data[2]), "Rejected: " + str(data[3]), "No response: " + str(no_response)]
        ),
        link = dict(
            #change last back to 1
        source = [0, 0, 0, 1],
        target = [3, 1, 4, 2],
        value = [data[3], data[1] + data[2], no_response, data[2]]
    ))])
    plt_html = po.plot(fig, filename='./application/templates/sankey.html', include_plotlyjs=True, output_type='div')
    return Markup(plt_html)

@app.route('/')
@app.route('/home')
def home():
    plt = make_sankey()
    return render_template('home.html', plt = plt)

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
        flash('You have inputted a new application for a role at ' + form.company.data.strip() + '!')
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

@app.route('/edit_application/<app_id>', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    app = Application.query.filter_by(id=app_id).first_or_404()
    form = UpdateApplicationForm(app.status)
    delete_form = DeleteApplicationForm()
    if delete_form.validate_on_submit():
        if delete_form.delete.data == "Yes":
            db.session.delete(app)
            db.session.commit()
            flash('You have deleted the application.')
            return redirect(url_for('dashboard'))
        else:
            flash('You have not deleted this application.')
            return redirect(url_for('edit_application', app_id=app.id))
    elif form.validate_on_submit():
        app.status = form.status.data
        app.last_updated = datetime.utcnow()
        db.session.commit()
        flash('You have updated the application\'s status to ' + form.status.data)
        return redirect(url_for('dashboard'))
    return render_template('edit_application.html', app=app, form=form, delete_form=delete_form, clean_date=clean_date)

@app.route('/analytics')
@login_required
def analytics():
    apps = list(current_user.positions_applied_to())
    companies = set([app.company for app in apps])
    data = [len([app for app in apps if app.status == "Applied"]), 
            len([app for app in apps if app.status == "Interviewing"]),
            len([app for app in apps if app.status == "Offer"]),
            len([app for app in apps if app.status == "Rejected"])]
    plt = make_sankey()
    return render_template('analytics.html', title='Home', user=current_user,
                           apps=apps, companies=companies, data=data, plt=plt)
