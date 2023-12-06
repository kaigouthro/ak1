import subprocess

# Install sqlalchemy if not already installed
try:
    import sqlalchemy
except ImportError:
    subprocess.run(["pip", "install", "sqlalchemy"])

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

class DBHandler:
    def __init__(self, database_type="sqlite", host="localhost", port=5432, user="admin", password="password", database="mydatabase"):
        self.database_type = database_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.database_path = self.generate_dbpath()

        self.engine = self.create_engine()
        self.session = self.create_session()
        self.Base = declarative_base()

    def generate_dbpath(self):
        scheme_templates = {
            "sqlite": "sqlite:///{database_path}",
            "postgresql": "postgresql://{user}:{password}@{host}:{port}/{database}",
            "mysql": "mysql://{user}:{password}@{host}:{port}/{database}",
            "snowflake": "snowflake://{user}:{password}@{account_id}/{database}"
        }
        return scheme_templates[self.database_type].format(
            database_path=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )

    def create_engine(self):
        engine = create_engine(self.database_path)
        return engine

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def _create_base(self):
        Base = declarative_base()
        return Base
