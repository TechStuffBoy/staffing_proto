import os
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from app import mail

import time


def send_async_email(app, msg):
    with app.app_context():
        # time.sleep(20)
        mail.send(msg)
        print('Mail is sent through the thread.')


def send_async_email_attachment(app, msg, attachment_list):
    with app.app_context():
        # time.sleep(20)
        mail.send(msg)
        print('Mail is sent through the thread.')
        for attachment in attachment_list:
            # print(f">>>>> {attachment}")
            if os.path.exists(attachment['location']):
                os.remove(attachment['location'])
                print(f"### Successfully Removed locally : {attachment['location']}")
            else:
                print(f"### Remove failed : {attachment['location']}")
        

def send_email(subject, sender, recipients_list, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients_list)
    msg.body = text_body
    msg.html = html_body
    # Note in thread, we need to pass the current_app
    Thread(target=send_async_email, args=(
        current_app._get_current_object(), msg)).start()


# [{'name': some_name1}, {'location' : some_location1}, {'name' : some_name2}, {'location' : some_location2}]
def send_email_attachment(subject, sender, recipients_list, text_body, html_body, attachment_list, mime_type='application/pdf'):
    """ This is a method to handle multiple attachments """
    """ To handle Msword documents as well """
    msg = Message(subject, sender=sender, recipients=recipients_list)
    msg.body = text_body
    msg.html = html_body
    for attachmet in attachment_list:
        with current_app.open_resource(attachmet['location']) as fp:
            msg.attach(attachmet['name'], mime_type, fp.read())
            # print(f"Attachment : {attachmet['location']} added.")
   # Note in thread, we need to pass the current_app
    Thread(target=send_async_email_attachment, args=(
        current_app._get_current_object(), msg, attachment_list)).start()
# application/msword


# send Password Reset email for employee
def send_password_reset_email(employee):
    token = employee.get_reset_password_token()
    send_email('Reset Your Password',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients_list=[employee.email],
               text_body=render_template('email/reset_password.txt',
                                         employee=employee, token=token),
               html_body=render_template('email/reset_password.html',
                                         employee=employee, token=token))
