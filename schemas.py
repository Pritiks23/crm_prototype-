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

## Properties stored as a dict ex: {
#   "status": "lead",
#   "lead_score": 85,
#   "region": "US"
# }

class ActivityCreate(BaseModel):
    type: str
    metadata: Dict
