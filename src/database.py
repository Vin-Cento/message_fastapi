from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from config import config

mysql_url = URL.create(
    "mysql",
    username=config["DB_USER_NAME"],
    password=config["DB_PASS_NAME"],
    host=config["DB_HOST_NAME"],
    database=config["DB_TESTS"],
)

engine = create_engine(mysql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
