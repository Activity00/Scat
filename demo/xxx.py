from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

print(locals())


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(20))

engin = create_engine('mysql://root:root@localhost:3306/sqlachelmytest')
DBSsession = sessionmaker(engin)

session = DBSsession()
new_user = User(name='xxxx')
session.add(new_user)
session.commit()
session.close()

