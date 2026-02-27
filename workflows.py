## listens to contact_updated, if status == "lead" creates activity entry
from event_bus import subscribe
from database import SessionLocal
from models import Activity

def contact_updated_handler(payload):
    db = SessionLocal()
    contact = payload["contact"]

    if contact.properties.get("status") == "lead":
        activity = Activity(
            contact_id=contact.id,
            type="workflow_triggered",
            metadata={"rule": "lead_status_detected"}
        )
        db.add(activity)
        db.commit()
    db.close()

def register_workflows():
    subscribe("contact_updated", contact_updated_handler)
