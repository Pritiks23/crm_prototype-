from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    tenant_id = Column(String, index=True)
    email = Column(String, index=True)
    properties = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    activities = relationship("Activity", back_populates="contact")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, default=generate_uuid)
    contact_id = Column(String, ForeignKey("contacts.id"))
    type = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    contact = relationship("Contact", back_populates="activities")
