
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey,Table

#The engine is created, this is the one that will translate python into SQL statements. This will talk directly to the database with SQL commands.
engine = create_engine('postgresql://leex:thinkful@localhost:5432/tbay')
#Session is the same as the psycopg2 cursor, this will queque and execute database transactions. Multiple sessions can take place on a singel database simultaneously.
Session = sessionmaker(bind=engine)
session=Session()
#This declarative base is like the model repository. This is the one that will create the create table statements, in order to build the database structure
Base=declarative_base()

"""
item_bidders_table = Table('item_bidders_association',Base.metadata,
    Column("bid_id",Integer,ForeignKey("bids.id")),
    Column("bidder_id",Integer,ForeignKey("users.id"))
)
"""


class Item(Base):
    __tablename__ = "items"

    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(String)
    start_time=Column(DateTime,default=datetime.utcnow)
    owner_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    bids=relationship("Bid",backref="target_item")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username= Column(String, nullable=False)
    password= Column(String,nullable=False)
    auctions=relationship("Item",backref="owner")
    bids=relationship("Bid",backref="bidder")
    #bids=relationship("Bid",secondary="item_bidders_association",backref="bidder")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer,primary_key=True)
    price= Column(Float, nullable=False)
    item_id=Column(Integer,ForeignKey('items.id'))
    bidder_id=Column(Integer,ForeignKey('users.id'))
    

Base.metadata.create_all(engine)

""""
In order to test the database run the following statements in python:

from tbay import session, User, Item, Bid
leo=User(username='Leonardo',password='1234')
mafer=User(username='Maria Fernanda',password='9345')
jp=User(username='Juan Pablo',password='vale1093pauletes')

compu=Item(name='Macbook Pro Retina',description='Una compu de 13 pulgadas casi nueva.')
celu=Item(name='Iphone SE',description='Un Iphone SE segunda generación.')
leo.auctions=[compu,celu]


oferta1=Bid()
oferta1.price=1500
mafer.bids=[oferta1]
compu.bids=[oferta1]

oferta2=Bid()
oferta2.price=1450
jp.bids=[oferta2]
celu.bids=[oferta2]

oferta3=Bid()
oferta3.price=1700
jp.bids=[oferta3]
celu.bids=[oferta3]

session.add_all([leo,mafer,jp,compu,celu,oferta1])

*****SQL STATEMENTS*****
select * from users;
select * from items;
select * from bids;
jp
select items.id, items.name, owners.username "owner" , bids.id,bids.price,buyers.username "buyer" 
from users "owners", users "buyers" ,bids, items, item_bidders_association 
where buyers.id=item_bidders_association.bidder_id 
and items.id=bids.item_id 
and owner_id=owners.id;


"""