
# FILE: database.py
# Database Configuration and Connection

import os
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def build_sqlalchemy_uri_from_env():

    # 1) Direct full URI override
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url

    # 2) MySQL config via env
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ.get('DB_NAME')

    # If user provided a DB name and user/password, construct a MySQL URI
    if db_user and db_password and db_name:
        # prefer pymysql driver if available
        return f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # 3) Fallback to SQLite in the project's db/ directory
    base = os.path.dirname(os.path.abspath(__file__))
    sqlite_path = os.path.join(base, 'db', 'ecotrack.sqlite')
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    return f'sqlite:///{sqlite_path}'


def init_db(app):

    app.config.setdefault('SQLALCHEMY_DATABASE_URI', build_sqlalchemy_uri_from_env())
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    # optional engine options from env (JSON string not required)
    db.init_app(app)
    return db


def create_tables(app):

    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")


def drop_tables(app):

    with app.app_context():
        db.drop_all()
        print("⚠️  All database tables dropped!")


def test_connection():

    try:
        connection = pymysql.connect(
            host=DatabaseConfig.DB_HOST,
            port=DatabaseConfig.DB_PORT,
            user=DatabaseConfig.DB_USER,
            password=DatabaseConfig.DB_PASSWORD,
            database=DatabaseConfig.DB_NAME
        )
        connection.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def get_db_session():

    return db.session


# Utility functions for database operations
class DatabaseUtils:

    @staticmethod
    def add_and_commit(obj):

        try:
            db.session.add(obj)
            db.session.commit()
            return True, "Success"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_and_commit(obj):

        try:
            db.session.delete(obj)
            db.session.commit()
            return True, "Success"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def commit():

        try:
            db.session.commit()
            return True, "Success"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def rollback():

        db.session.rollback()


# For direct script execution (testing)
if __name__ == "__main__":
    print("Testing database connection...")
    test_connection()