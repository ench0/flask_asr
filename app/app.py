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

from config import Configuration # import our configuration data.

app = Flask(__name__)

app.config.from_object(Configuration) # use values from our Configuration object.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)