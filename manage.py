'''
Controls database migrations
After making changes in DDL, run this file
'''
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pigge.main import APP, db


migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
