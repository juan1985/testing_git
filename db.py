from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import Config
from app import app, db
from app.models import User, Role
from flask_security import SQLAlchemyUserDatastore

SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

migrate = Migrate(app, db)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
