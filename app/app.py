from flask import Flask, g
from flask_login import LoginManager, current_user
# from flask.ext.login import LoginManager, current_user # depreciated
# pip install Flask-Login

# from flask.ext.migrate import Migrate, MigrateCommand # depreciated
from flask_migrate import Migrate, MigrateCommand
# from flask.ext.script import Manager # depreciated
from flask_script import Manager
# pip install flask-migrate

# from flask.ext.sqlalchemy import SQLAlchemy # depreciated
from flask_sqlalchemy import SQLAlchemy
# pip install sqlalchemy
# pip install flask-sqlalchemy

from flask_bcrypt import Bcrypt
# from flask.ext.bcrypt import Bcrypt # depreciated
# pip install flask-bcrypt

from config import Configuration # import our configuration data.

app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config.from_object(Configuration) # use values from our Configuration object.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Add to the end of the module.
login_manager = LoginManager(app)
login_manager.login_view = "login"
@app.before_request
def _before_request():
    g.user = current_user