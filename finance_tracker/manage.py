from app import create_app, db
from flask_migrate import Migrate, init as migrate_init

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        migrate_init()