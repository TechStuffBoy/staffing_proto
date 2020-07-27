from flask import flash, redirect, render_template, url_for, Markup, abort
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm

from .. import db
from ..models import Employee

from ..email import send_password_reset_email

@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    # Prevent the view by non-admin, we want only admin to register new employees.
    if not current_user.is_admin:
        abort(403)

    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data, username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data)

        # Add employee to database
        db.session.add(employee)
        db.session.commit()
        flash(Markup(
            '<p style="text-align:center;">Employee registered successfully!</p>'), 'success')

        # redirect to the register page for the admin to add any further employees.
        return redirect(url_for('auth.register'))

    # on GET request, render the registeration html page
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()

        if employee is not None and employee.verify_password(form.password.data):
            # Allow employee to login
            login_user(employee)

            # redirect to the appropriate dashboard page
            if employee.is_admin:
                return redirect(url_for('public.admin_dashboard'))
            else:
                return redirect(url_for('public.dashboard'))
        else:
            flash(Markup(
                '<p style="text-align:center;">Ivalid Email or password.</p>'), 'danger')
    # on GET, load login html template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash(Markup(
        '<p style="text-align:center;">You have successfully been logged out.</p>'), 'success')

    # redirect to the login page
    return redirect(url_for('auth.login'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            send_password_reset_email(employee)
        # Note here, even if we enter wrong email, we will gonna display that success image.
        flash(Markup(
            '<p style="text-align:center;">Check your email for the instructions to reset your password.</p>'), 'success')
        return redirect(url_for('auth.login'))
    # On GET request
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    employee = Employee.verify_reset_password_token(token)
    if not employee:
        return redirect(url_for('public.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        employee.password = form.password.data
        db.session.commit()
        flash(Markup(
            '<p style="text-align:center;">Your password has been reset.</p>'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

    

