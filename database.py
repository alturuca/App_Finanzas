from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL para MySQL (XAMPP)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/finanzas_db"

# EL MOTOR: Eliminamos connect_args porque en MySQL no se necesitan
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()