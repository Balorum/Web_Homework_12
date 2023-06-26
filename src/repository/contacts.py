from typing import List
from sqlalchemy import and_
from datetime import date, datetime
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, user: User, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_days_to_birthday(skip: int, user: User, limit: int, db: Session) -> List[Contact]:
    birthday_days = []
    nowdays_date = datetime.now().date()
    days = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    for i in days:
        birtday_year = date(year=i.birthday.year+(nowdays_date.year-i.birthday.year), month=i.birthday.month, day=i.birthday.day)
        if (birtday_year-nowdays_date).days <=7 and (birtday_year-nowdays_date).days >=0:
            birthday_days.append(i)
    return birthday_days

async def get_by_name(skip: int, user: User, limit: int, name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_by_surname(skip: int, user: User, limit: int, surname: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_by_email(skip: int, user: User, limit: int, email: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, phone_number=body.phone_number,\
                      email=body.email, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name=body.name, 
        contact.surname=body.surname, 
        contact.phone_number=body.phone_number,
        contact.email=body.email, 
        contact.birthday=body.birthday
        db.commit()
    return contact
