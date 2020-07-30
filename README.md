# Welcome to the staffingProto
This is a staffing Industry Prototype that i copied from my Private Repo.

It has the following supports,
```
 > Generic public pages for the public.
 > Employee Management system.
 > Contact Form.
 > Post resume Form.
 > When public submit contact form or resume form, the Employees will get notified through the Mail.
 > Only Admin can register new employess.
 > Employess are provied with reset password functionality to change password first-time or if they forgot the password.
 ```
To do functionalities,
```
 > Improvise UI further.
 > Add "post-job" functionality to the employees, so that they can post their job requirements from client to the public.
 > Add leave management system.
 ```
 
 This web-app is completely developed using the **Flask Web Framework**.
 
 Some major extentions used,
 ```
  > Flask-SQLalchemy
  > Flask-Migrate
  > Flask-Mail
  > Flask-Login
  > Flask-WTF
  > Bootstrap-Flask [Bootstrap 4]
  > psycopg2
  > gunicorn
  ```
  ```
  This production repo is deployed in AWS and it is just a copy of it.
  For the development SQLite database was used and Postgres has been chosen for the production and it is running with gunicorn.
  ```
  
