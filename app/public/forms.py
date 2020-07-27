import os
from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email
from wtforms import ValidationError

from flask_wtf.file import FileField, FileRequired
import phonenumbers

from flask import current_app, render_template
from werkzeug.utils import secure_filename

from ..email import send_email_attachment, send_email


STATE_CHOICES = [('--Choose--', '--Choose--'), ("AL - Alabama", "AL - Alabama"), ("AK - Alaska", "AK - Alaska"), ("AZ - Arizona", "AZ - Arizona"), ("AR - Arkansas", "AR - Arkansas"), ("CA - California", "CA - California"), ("CO - Colorado", "CO - Colorado"),
                 ("CT - Connecticut", "CT - Connecticut"), ("DC - Washington DC", "DC - Washington DC"), ("DE - Deleware", "DE - Deleware"), ("FL - Florida", "FL - Florida"), ("GA - Georgia", "GA - Georgia"),
                 ("HI - Hawaii", "HI - Hawaii"), ("ID - Idaho", "ID - Idaho"), ("IL - Illinios", "IL - Illinios"), ("IN - Indiana", "IN - Indiana"), ("IA - Iowa", "IA - Iowa"), ("KS - Kansas", "KS - Kansas"), ("KY - Kentucky", "KY - Kentucky"), ("LA - Louisiana", "LA - Louisiana"), ("ME - Maine", "ME - Maine"), ("MD - Maryland", "MD - Maryland"), ("MO - Missouri", "MO - Missouri"), ("MT - Montana", "MT - Montana"), ("NE - Nebraska", "NE - Nebraska"), ("NV - Nevada", "NV - Nevada"), ("NH - New Hampshire", "NH - New Hampshire"),("MA - Massachusetts", "MA - Massachusetts"), ("MI - Michigan", "MI - Michigan"), ("MN - Minnesota", "MN - Minnesota"), ("MS - Mississippi", "MS - Mississippi"),("NJ - New Jersey", "NJ - New Jersey"), ("NM - New Mexico", "NM - New Mexico"), ("NY - New York", "NY - New York"), ("NC - North Carolina", "NC - North Carolina"),
                 ("ND - North Dakota", "ND - North Dakota"), ("OH - Ohio", "OH - Ohio"), ("OK - Oklahoma","OK - Oklahoma"), ("OR - Oregon", "OR - Oregon"), ("PA - Pennsylvania", "PA - Pennsylvania"),("RI - Rhode Island", "RI - Rhode Island"), ("SC - South Carolina","SC - South Carolina"), ("SD - South Dakota", "SD - South Dakota"), ("TN-Tennessee", "TN-Tennessee"),
                 ("TX - Texas", "TX - Texas"), ("UT - Utah", "UT - Utah"), ("VT - Vermont", "VT - Vermont"), ("VA - Virgina", "VA - Virgina"), ("WA - Washington", "WA - Washington"), ("WV - West Virginia", "WV - West Virginia"),
                 ("WI - Wisconsin", "WI - Wisconsin"), ("WY - Wyoming", "WY - Wyoming")]


class PostResumeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="Please enter first name.")])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact_number = StringField(
        'Contact Number', validators=[DataRequired(), Length(min=10,max=10)])
    alternate_contact_number = StringField(
        'Alternate Contact Number(if any)', validators=[Length(min=10, max=10)])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    alternate_email = StringField('Alternate Contact Email(if any)', validators=[ Email()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField(
        'State', validators=[DataRequired()], choices=STATE_CHOICES)
    visa_status = SelectField('Visa Status', validators=[DataRequired()],
                              choices=[('--Choose--', '--Choose--'), ('ACTIVE', 'ACTIVE'),
                                 ('EXPIRED', 'EXPIRED'),
                                 ('INVALID', 'INVALID')])
    current_status = SelectField('Current Status (*): (Working or not ) :', validators=[DataRequired()],
                                 choices=[('--Choose--', '--Choose--'),('WORKING', 'WORKING'),
                                          ('NOT WORKING', 'NOT WORKING'),
                                       ('NOTICE PERIOD', 'NOTICE PERIOD')])
    job_title = StringField('Job Title', validators=[DataRequired()])
    available = SelectField('Availability to start the project (*) :', validators=[DataRequired()],
                            choices=[('--Choose--', '--Choose--'), ('YES', 'YES'),
                                          ('NO', 'NO'),
                                          ])
    cover_letter = FileField(validators=[FileRequired()])
    resume = FileField(validators=[FileRequired()])
    summary = TextAreaField('Summary')
    submit = SubmitField('Post Resume')

    def validate_contact_number(form, field):
        # print(f"Debug1 : Outside validate_contact_number")
        # print(f"Debug11 : {field.data}")
        if len(field.data) > 10:
            # print(f"Debug2 : Inside validate_contact_number")
            raise ValidationError('Phone number should be 10 digit long.')

    def validate_alternate_contact_number(form, field):
        # print(f"Debug1 : Outside validate_contact_number")
        # print(f"Debug11 : {field.data}")
        if len(field.data) > 10:
            # print(f"Debug2 : Inside validate_contact_number")
            raise ValidationError('Phone number should be 10 digit long.')

    def validate_state(form, field):
        # print(f"Debug3 : Outside validate_state")
        if field.data == '--Choose--':
            # print(f"Debug4 : Inside validate_state")
            raise ValidationError('Please choose atleast one.')
        # print(f"Debug12 : {field.data}")

    def validate_visa_status(form, field):
        # print(f"Debug5 : Outside validate_state")
        if field.data == '--Choose--':
            # print(f"Debug6 : Inside validate_state")
            raise ValidationError('Please choose atleast one.')
        # print(f"Debug13 : {field.data}")

    
    def validate_current_status(form, field):
        # print(f"Debug7 : Outside validate_current_status")
        if field.data == '--Choose--':
            # print(f"Debug8 : Inside validate_current_status")
            raise ValidationError('Please choose atleast one.')
        # print(f"Debug14 : {field.data}")

    def validate_available(form, field):
        # print(f"Debug9 : Outside validate_available")
        if field.data == '--Choose--':
            # print(f"Debug9 : Inside validate_available")
            raise ValidationError('Please choose atleast one.')
        # print(f"Debug15 : {field.data}")


    def allowed_image(self, filename):
        if not "." in filename:
            return False
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False

    def allowed_file(self, filename):
        if not "." in filename:
            return False
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in current_app.config["ALLOWED_FILE_EXTENSIONS"]:
            return True
        else:
            return False

    def upload_image(self, image):
        if self.allowed_image(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(
                current_app.config["IMAGE_UPLOADS"], filename))
            print("Image saved")
        else:
            print("Image was not saved.")

    def upload_file(self, ifile):
        # Make instance directory
        if not os.path.exists(current_app.config["FILE_UPLOADS"]):
            os.makedirs(current_app.config["FILE_UPLOADS"])
        else:
            print(f"{current_app.config['FILE_UPLOADS']} already exists.")
        if self.allowed_file(ifile.filename):
            filename = secure_filename(ifile.filename)
            ifile.save(os.path.join(
                current_app.config["FILE_UPLOADS"], filename))
            print("File saved")
        else:
            print("File was not saved.")

    def post_mail(self, cover_letter, resume, form):
        base_dir = current_app.config["FILE_UPLOADS"]
        attachment_list = []
        attachment_list.append({'name': 'cover_letter', 'location': os.path.join(
            base_dir, secure_filename(cover_letter.filename))})
        attachment_list.append({'name': 'resume', 'location': os.path.join(
            base_dir, secure_filename(resume.filename))})
        print(f"In Post Mail..")
        for attachment in attachment_list:
            print(f"post mail >>>> {attachment}")
        # Send email
        send_email_attachment("We recieved Resume.", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients_list=['nandhu.misc@gmail.com'], text_body=render_template(
            'email/recieved_resume.txt', first_name="Nandha", recruiter_name='Dhamu', form=form), html_body=render_template('email/recieved_resume.html', first_name="Nandha", recruiter_name='Dhamu', form=form), attachment_list=attachment_list)


class ContactUsForm(FlaskForm):
    first_name = StringField('First Name (*)', validators=[
                             DataRequired(message="Please enter first name.")])
    contact_number = StringField(
        'Contact Number (*)', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField('Contact Email (*)',
                        validators=[DataRequired(), Email()])
    state = SelectField(
        'State (*)', validators=[DataRequired()], choices=STATE_CHOICES)
    city = StringField('City (*)', validators=[DataRequired()])
    comments = TextAreaField('Comments (If any):')
    submit = SubmitField('SEND')

    def validate_contact_number(form, field):
        if len(field.data) > 10:
            raise ValidationError('Phone number should be 10 digit long.')
    
    def validate_state(form, field):
        if field.data == '--Choose--':
            raise ValidationError('Please choose atleast one.')
    
    def post_greeting_mail(self, form):
        try:
            # Send Notification to NTech
            send_email("We got a customer Query!!", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients_list=[
                       'free2dhamu@gmail.com', 'nandhu.misc@gmail.com'], text_body=render_template('email/recieved_contact.txt', form=form), html_body=render_template('email/recieved_contact.html', form=form))
            
            # Send Greetings to Candidate
            send_email("Greetings from Ntech Global.", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients_list=[form.email.data], text_body=render_template(
                'email/greet_candidate.txt', form=form), html_body=render_template('email/greet_candidate.html', form=form))
            

        except:
            print(f"Exception occured, May be check the contact mail={form.email.data}")



   
