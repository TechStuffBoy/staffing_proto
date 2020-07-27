import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')

app = create_app(config_name)
print(f"SQLALCHEMY_DATABASE_URI={app.config['SQLALCHEMY_DATABASE_URI']}")


# To add the flask shell context
from app import db
from app.models import Employee, Department, Role


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee, 'Department': Department, 'Role' : Role}

