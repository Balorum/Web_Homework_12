from typing import List
from src.services.auth import auth_service
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, current_user, limit, db)
    return contacts

@router.get("/days_to_birthday", response_model=List[ContactResponse])
async def read_birthdays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_days_to_birthday(skip, current_user, limit, db)
    return contacts

@router.get("/get_by_name", response_model=List[ContactResponse])
async def read_names(skip: int = 0, limit: int = 100, name: str = "Olya", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_by_name(skip, current_user, limit, name, db)
    return contacts

@router.get("/get_by_surname", response_model=List[ContactResponse])
async def read_surname(skip: int = 0, limit: int = 100, surname: str = "Ivanov", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_by_surname(skip, current_user, limit, surname, db)
    return contacts

@router.get("/get_by_email", response_model=List[ContactResponse])
async def read_email(skip: int = 0, limit: int = 100, email: str = "TestEmail@gmail.com", db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_by_email(skip, current_user, limit, email, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),\
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact