import subprocess

# Install sqlalchemy if not already installed

try:
    pass

except ImportError:
    subprocess.run(["pip", "install", "sqlalchemy"])

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


class DbHandler:
    """
    A class for handling database operations.

    Args:
        database_type (str): The type of the database. Defaults to "sqlite".
        host (str): The host of the database. Defaults to "localhost".
        port (int): The port of the database. Defaults to 5432.
        user (str): The username for accessing the database. Defaults to "admin".
        password (str): The password for accessing the database. Defaults to "password".
        database (str): The name of the database. Defaults to "mydatabase".

    Attributes:
        engine: The database engine.
        session: The database session.
        Base: The base class for declarative models.

    Methods:
        generate_dbpath           : Generates the database path based on the specified database type.
        create_engine             : Creates the database engine.
        create_session            : Creates the database session.
        upsert                    : Inserts or updates data in the specified table.
        get_all                   : Retrieves all records from the specified table.
        get_by_id                 : Retrieves a record from the specified table by its ID.
        delete_by_id              : Deletes a record from the specified table by its ID.
        delete_all                : Deletes all records from the specified table.
        get_all_with_relationships: Retrieves all records from the specified table with their relationships.

    Examples:
        >>> db = DbHandler()
        >>> db.upsert(User, {"id": 1, "name": "John"})
        >>> db.get_all(User)
        [<User(id=1, name='John')>]
    """

    def __init__(
        self,
        database_type="sqlite",
        host="localhost",
        port=5432,
        user="admin",
        password="password",
        database="mydatabase",
    ):
        self.database_type = database_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.database_path = self.generate_dbpath()

        self.Base = declarative_base()

    @staticmethod
    def generate_dbpath(
        database_type="sqlite",
        host="localhost",
        port=5432,
        user="admin",
        password="password",
        database="mydatabase",
    ):
        scheme_templates = {
            "sqlite": "sqlite:///{database_path}",
            "postgresql": "postgresql://{user}:{password}@{host}:{port}/{database}",
            "mysql": "mysql://{user}:{password}@{host}:{port}/{database}",
            "snowflake": "snowflake://{user}:{password}@{account_id}/{database}",
        }
        return scheme_templates[database_type].format(
            database_path=database,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )

    def create_engine(self):
        return create_engine(self.database_path)

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    @staticmethod
    def _create_base():
        return declarative_base()

    def load_db(self, db_path):
        self.database_path = db_path
        self.engine = self.create_engine()
        self.session = self.create_session()
        self.Base = self._create_base()

    def upsert(self, table, data):
        try:
            if isinstance(data, list):
                for d in data:
                    self.session.merge(table(**d))
            else:
                self.session.merge(table(**data))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_all(self, table):
        try:
            return self.session.query(table).all()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_by_id(self, table, id):
        try:
            return self.session.query(table).get(id)
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def delete_by_id(self, table, id):
        try:
            self.session.query(table).filter(table.id == id).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def delete_all(self, table):
        try:
            self.session.query(table).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_all_with_relationships(self, table):
        try:
            return self.session.query(table).options(relationship(table.relationship_name)).all()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
