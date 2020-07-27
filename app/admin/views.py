from flask import abort, flash, redirect, render_template, url_for, Markup
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    # load departments template
    return render_template('/admin/departments/departments.html', departments=departments, title='Departments')

# Add Department
@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)

        try:
            # Add department to the database
            db.session.add(department)
            db.session.commit()
            flash(Markup(
                '<p style="text-align:center;">You have successfully added a new department.</p>'), 'success')
        except:
            # in case department already exists
            flash(Markup(
                '<p style="text-align:center;">Error: department name already exists.</p>'), 'danger')
        # return to departments page
        return redirect(url_for('admin.list_departments'))
    

    # load the department template
    return render_template('admin/departments/department.html', action="Add", add_department=add_department, form=form, title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()
    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department) # we pass department because, if we dont pass, it will only be a empty form, since we are editing, we need previous data to be present when we give it to the admin user.

    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash(Markup(
            '<p style="text-align:center;">You have successfully edited the department.</p>'), 'success')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    # For GET, just filling the form with existing data
    form.description.data = department.description
    form.name.data = department.name

    return render_template('admin/departments/department.html', action='Edit', add_department=add_department, form=form, department=department, title='Edit Department')

# Delete department
@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash(Markup(
        '<p style="text-align:center;">You have successfully deleted the department.</p>'), 'success')
    
    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    # Need to check once
    return render_template(title="Delete Department")

# Role views

# List roles
@admin.route('/roles', methods=['GET', 'POST'])
@login_required
def list_roles():
    """
    List all roles
    """
    check_admin()

    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Role')

# Add role
@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True
    form = RoleForm()

    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            # Add Role to the database
            db.session.add(role)
            db.session.commit()
            flash(Markup(
                '<p style="text-align:center;">You have successfully added a new Role.</p>'), 'success')
        except:
            # in case, role already exists
            flash(Markup(
                '<p style="text-align:center;">Error: role name already exists.</p>'), 'danger')
        return redirect(url_for('admin.list_roles'))
    # for GET call
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add Role')

# Edit role
@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash(Markup(
            '<p style="text-align:center;">You have successfully edited a role.</p>'), 'success')

        # redirect to the list role page
        return redirect(url_for('admin.list_roles'))
    # Fill the existing data
    form.description.data = role.description
    form.name.data = role.name
    
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title="Edit Role")

# Delete Role
@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash(Markup(
        '<p style="text-align:center;">You have successfully deleted a role.</p>'), 'success')
    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

# Employee Views

@admin.route('/employee')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html', employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)
    
    form = EmployeeAssignForm(obj=employee)

    if form.validate_on_submit():
        # Note : This role and departmet are accessed through the reltion we have in model.
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash(Markup(
            '<p style="text-align:center;">You have successfully assigned a department and role.</p>'), 'success')
        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))
    
    return render_template('admin/employees/employee.html', employee=employee, form=form, title='Assign Employee')


