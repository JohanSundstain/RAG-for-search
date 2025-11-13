from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Text
from .db import Base

class Texts(Base):
    __tablename__ = "texts"

    pk_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), default="")
    textt: Mapped[str] = mapped_column(Text, default="")
    sourcee: Mapped[str] = mapped_column(String(64), default="")
    
