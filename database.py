import os
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, Unicode

# Készítsük el a motort, amely adatokat fog tárolni lokális db-ban
motor = create_engine('sqlite:///csoportok.db',echo = True)
Base = declarative_base()
metadata= Base.metadata

class ListGroups(object):

    def __init__(self, id, name, contact_name, address, email, phone, service, full_price_members,
                 discount_price_members, date, time, payed, created, modified, description ):
        self.id = id
        self.name = name
        self.contact_name = contact_name
        self.address = address
        self.email = email
        self.phone = phone
        self.service = service
        self.full_price_members = full_price_members
        self.discount_price_members = discount_price_members
        self.date = date
        self.time = time
        self.payed = payed
        self.created = created
        self.modified = modified
        self.description = description


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable= False)
    contact_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String(30), nullable=False)
    phone = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    payed = Column(Boolean)
    created = Column(Date)
    modified = Column(Date)
    service = Column(String(20), nullable=False)
    full_price = Column(Integer, nullable=False)
    discount_price = Column(Integer, nullable=False)
    description = Column(String)



# Készítsük el az összes táblát
Base.metadata.create_all(motor)