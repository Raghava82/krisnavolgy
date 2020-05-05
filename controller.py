from database import *
from sqlalchemy.orm import sessionmaker

def add_group(session, data):
    """
   Adding a group
    """
    groups = Groups()
    groups.name = data["groups"]["name"]
    groups.contact_name = data["groups"]["contact_name"]
    groups.address = data["groups"]["address"]
    groups.email = data["groups"]["email"]
    groups.phone = data["groups"]["phone"]
    groups.description = data["groups"]["description"]
    groups.full_price = data["groups"]["full_price"]
    groups.discount_price = data["groups"]["discount_price"]
    groups.date= data["groups"]["date"]

    session.add(groups)
    session.commit()



def connect_to_database():
    """
    #Connect to our SQLite database and return a Session object
    """
    engine = create_engine("sqlite:///csoportok.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def delete_record(session, id_num):
    """
    Delete a record from the database
    """
    record = session.query(Groups).filter_by(id=id_num).one()
    session.delete(record)
    session.commit()


def edit_record(session, id_num, row):
    """
    Edit a record
    """
    record = session.query(Groups).filter_by(id=id_num).one()
    record.name = row["name"]
    record.contact_name = row["contact_name"]
    record.address = row["address"]
    record.email = row["email"]
    record.phone = row["phone"]
    record.service = row["service"]
    record.full_price = row["full_price"]
    record.discount_price = row["discount_price"]
    record.date = row["date"]
    record.time = row["time"]
    record.payed = row["payed"]
    record.created = row["created"]
    record.modified = row["modified"]
    record.description = row["description"]
    session.add(record)
    session.commit()

def get_all_records(session):
    """
    Get all records and return them
    """
    result = session.query(Groups).all()
    return result


def search_records(session, filter_choice, keyword):
    """
    Searches the database based on the filter chosen and the keyword
    given by the user
    """
    if filter_choice == "Csoport":
        qry = session.query(Groups)
        result = qry.filter(Groups.name.contains('%s' % keyword)).all()
        records = []
        for record in result:
            for group in record.groups:
                records.append(group)
        result = records
    elif filter_choice == "Dátum":
        qry = session.query(Groups)
        result = qry.filter(Groups.date.contains('%s' % keyword)).all()

    elif filter_choice == "Szolgáltatás":
        qry = session.query(Groups)
        result = qry.filter(Groups.service.contains('%s'% keyword)).all()

    else:
        qry = session.query(Groups)
        result = qry.filter(Groups.payed.contains('%s' % keyword)).all()

    return result

def setup_database():
    """"""
    metadata.create_all()
