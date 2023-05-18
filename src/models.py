from sqlalchemy.dialects.mysql import CHAR, VARCHAR
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# model
class User_DB(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    username = Column(
        String(40).with_variant(VARCHAR(40, charset="utf8"), "mysql", "mariadb"),
        nullable=False,
    )
    # TODO: add email
    # email = Column()
    password = Column(
        String(60).with_variant(CHAR(60, charset="utf8"), "mysql", "mariadb"),
        nullable=False,
    )


class Message_DB(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True)
    message = Column(
        String(40).with_variant(VARCHAR(40, charset="utf8"), "mysql", "mariadb"),
        nullable=False,
    )
    # TODO: link message to user_id
    # relationship
    # user_id = Column(Integer)
