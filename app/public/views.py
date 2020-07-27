import os
from flask import render_template, flash, redirect, url_for, Markup, abort
from . import public

from flask import current_app
from werkzeug.utils import secure_filename

from .forms import PostResumeForm, ContactUsForm


from ..email import send_email, send_email_attachment

from flask_login import login_required, current_user


path1 = '/Users/techstuffboy/GithubRepository/ntekglobal_development/instance/file_uploads/CSS_Box_Model_Cheat_Sheet_-_Light.pdf'
path2 = '/Users/techstuffboy/GithubRepository/ntekglobal_development/instance/file_uploads/CSS_Selector_Cheat_Sheet_-_Light.pdf'

location_list = [{'name': 'cover_letter', 'location': path1},
                 {'name': 'resume', 'location': path2}]

@public.route('/')
def index():
    # send_email_attachment("We recieved Resume.", sender=current_app.config['MAIL_USERNAME'], recipients_list=['nandhu.misc@gmail.com'], text_body=render_template(
    #     'email/recieved_resume.txt', first_name="Nandha", recruiter_name='Dhamu'), html_body=render_template('email/recieved_resume.html', first_name="Nandha", recruiter_name='Dhamu'), attachment_list=location_list)
    return render_template('public/index.html', title='Home')


@public.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('public/dashboard.html', title="Dashboard")

@public.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    return render_template('public/admin_dashboard.html', title='Dashboard')



@public.route('/staffing/contract')
def contract_staffing():
    return render_template('public/services/contract_staffing.html', title='Contract Staffing')

# Services Views Starts

@public.route('/staffing/permanent')
def permanent_staffing():
    return render_template('public/services/permanent_staffing.html', title='Permanent Staffing')


@public.route('/hiring/cxo')
def cxo_hiring():
    return render_template('public/services/cxo_hiring.html', title='CXO Hiring')


@public.route('/hiring/executive')
def executive_hiring():
    return render_template('public/services/executive_hiring.html', title='Executive Hiring')


@public.route('/model/engagement')
def engagement_model():
    return render_template('public/services/engagement_model.html', title='Engagement Model')

# Services Views Ends

@public.route('/whyus')
def whyus():
    return render_template('public/whyus.html', title='Why NTech')


@public.route('/career')
def career():
    return render_template('public/career.html', title='Career')

@public.route('/post_resume', methods=['GET', 'POST'])
def post_resume():
    form = PostResumeForm()

    # print(form.errors)

    if form.validate_on_submit():
        base_dir = current_app.config["FILE_UPLOADS"]
        resume = form.resume.data
        attachment_list = []
        print(f"Resume={resume}")
        print(f"Resume name={resume.filename}")
        """ resume.filename prints CSS Selector Cheat Sheet - Light.pdf"""
        cover_letter = form.cover_letter.data
        form.upload_file(resume)
        form.upload_file(cover_letter)
        form.post_mail(cover_letter=cover_letter, resume=resume, form=form )
        flash(Markup(
            '<p style="text-align:center;">We got your Resume.</p>'), 'success')
        return redirect(url_for('public.whyus'))

    return render_template('public/post_resume.html', form=form, title='Post Resume')


@public.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactUsForm()
    # print(form.errors)

    if form.validate_on_submit():
        base_dir = current_app.config["FILE_UPLOADS"]
        flash(Markup(
            '<p style="text-align:center;">Thanks for contacting us.</p>'), 'success')
        form.post_greeting_mail(form=form)
        return redirect(url_for('public.whyus'))

    return render_template('public/contact_us.html', form=form, title='Contact Us')
