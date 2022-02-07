from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

#The engine is created, this is the one that will translate python into SQL statements. This will talk directly to the database with SQL commands.
engine = create_engine('postgresql://leex:thinkful@localhost:5432/tbay')
#Session is the same as the psycopg2 cursor, this will queque and execute database transactions. Multiple sessions can take place on a singel database simultaneously.
Session = sessionmaker(bind=engine)
session=Session()
#This declarative base is like the model repository. This is the one that will create the create table statements, in order to build the database structure
Base=declarative_base()

class Item(Base):
    __tablename__ = "items"

    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(String)
    start_time=Column(DateTime,default=datetime.utcnow)

Base.metadata.create_all(engine)