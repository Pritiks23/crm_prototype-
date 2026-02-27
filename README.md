# How To Run pip install fastapi uvicorn sqlalchemy pydantic uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

# What happens if two updates happen simultaneously? add Optimistic Locking, version = Column(Integer)

#  2️⃣ How do we shard by tenant?  
Shard by tenant by hashing the tenant_id (e.g., hash(tenant_id) % N) and routing all of that tenant’s data to a specific database shard, ensuring all their contacts and activities live together. This allows horizontal scaling because as we add more shards, we redistribute tenants across them without breaking tenant-level data isolation.

#  #3 How do we ensure idempotent workflows? Solution: Idempotency Key

Add unique constraint:

(workflow_id, contact_id)

Before running workflow:

Check if activity already exists.

# 4 How do we scale activity storage to billions of rows? Step 1 — Partitioning

Partition by:

tenant_id

or created_at (time-based), Step 2 — Cold Storage

Older than 1 year?

Move to:

Data warehouse

S3
