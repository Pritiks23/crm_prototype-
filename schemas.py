## Models = database shape
##Schemas = API shape
from pydantic import BaseModel
from typing import Dict, Optional

class ContactCreate(BaseModel):
    tenant_id: str
    email: str
    properties: Dict

class ContactUpdate(BaseModel):
    properties: Optional[Dict]

class ActivityCreate(BaseModel):
    type: str
    metadata: Dict
