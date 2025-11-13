from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import config

DATABASE_URL = (
    f"postgresql+psycopg://{config["USER"]}:{config["PASSWORD"]}"
    f"@{config["HOST"]}:{config["PORT"]}/{config["DB_NAME"]}"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
