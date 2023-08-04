from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

sqlite_database_name = "database.sqlite3"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_database_name)}"
print(database_url)

engine = create_engine(database_url, connect_args={"check_same_thread": False}, echo=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# no utilizar aca
base = declarative_base()