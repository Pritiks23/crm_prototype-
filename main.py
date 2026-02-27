from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Contact, Activity
from schemas import ContactCreate, ContactUpdate, ActivityCreate
from event_bus import publish
from workflows import register_workflows

Base.metadata.create_all(bind=engine)
register_workflows()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Contact
@app.post("/contacts")
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


# Update Contact (Triggers Workflow)
@app.patch("/contacts/{contact_id}")
def update_contact(contact_id: str, data: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")

    if data.properties:
        contact.properties = data.properties

    db.commit()
    db.refresh(contact)

    publish("contact_updated", {"contact": contact})

    return contact


# Delete Contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(contact)
    db.commit()
    return {"deleted": True}


# Search + Filter
@app.get("/contacts")
def search_contacts(
    tenant_id: str,
    email: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Contact).filter(Contact.tenant_id == tenant_id)

    if email:
        query = query.filter(Contact.email.contains(email))

    return query.all()


# Track Activity
@app.post("/contacts/{contact_id}/activities")
def add_activity(contact_id: str, data: ActivityCreate, db: Session = Depends(get_db)):
    activity = Activity(
        contact_id=contact_id,
        type=data.type,
        metadata=data.metadata
    )
    db.add(activity)
    db.commit()
    return activity


# View Activity History
@app.get("/contacts/{contact_id}/activities")
def get_activities(contact_id: str, db: Session = Depends(get_db)):
    return db.query(Activity).filter(Activity.contact_id == contact_id).all()
