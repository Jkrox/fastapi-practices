from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://fl0user:l8WFuke4sgwa@ep-proud-hat-80450834.us-east-2.aws.neon.tech:5432/postgres-movies?sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# no utilizar aca
base = declarative_base()
