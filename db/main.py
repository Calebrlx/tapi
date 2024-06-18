from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

DATABASE_URL = "mysql+mysqlconnector://root:abghse@10.0.0.25/sales_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class ProspectStatus(enum.Enum):
    not_contacted = "not_contacted"
    contacted = "contacted"
    followed_up = "followed_up"
    unresponsive = "unresponsive"

class LeadStatus(enum.Enum):
    responded = "responded"
    in_progress = "in_progress"
    closed_won = "closed_won"
    closed_lost = "closed_lost"

class Prospect(Base):
    __tablename__ = "prospects"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(Enum(ProspectStatus), default=ProspectStatus.not_contacted, nullable=False)
    contact_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer, ForeignKey("prospects.id"), nullable=False)
    messages = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    status = Column(Enum(LeadStatus), default=LeadStatus.responded, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    prospect = relationship("Prospect")

Base.metadata.create_all(bind=engine)

class ProspectCreate(BaseModel):
    slug: str

class ProspectUpdate(BaseModel):
    status: ProspectStatus

class LeadCreate(BaseModel):
    prospect_id: int
    messages: str
    notes: str

@app.post("/prospects/", response_model=dict)
def create_prospect(prospect: ProspectCreate):
    db = SessionLocal()
    db_prospect = Prospect(slug=prospect.slug)
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    db.close()
    return {"id": db_prospect.id, "slug": db_prospect.slug, "status": db_prospect.status.value}

@app.put("/prospects/{prospect_id}", response_model=dict)
def update_prospect(prospect_id: int, prospect: ProspectUpdate):
    db = SessionLocal()
    db_prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if db_prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    db_prospect.status = prospect.status
    db.commit()
    db.refresh(db_prospect)
    db.close()
    return {"id": db_prospect.id, "slug": db_prospect.slug, "status": db_prospect.status.value}

@app.post("/leads/", response_model=dict)
def create_lead(lead: LeadCreate):
    db = SessionLocal()
    db_lead = Lead(prospect_id=lead.prospect_id, messages=lead.messages, notes=lead.notes)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    db.close()
    return {"id": db_lead.id, "prospect_id": db_lead.prospect_id, "messages": db_lead.messages, "notes": db_lead.notes, "status": db_lead.status.value}

@app.get("/prospects/", response_model=list)
def read_prospects(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    prospects = db.query(Prospect).offset(skip).limit(limit).all()
    db.close()
    return [{"id": prospect.id, "slug": prospect.slug, "status": prospect.status.value, "contact_count": prospect.contact_count} for prospect in prospects]

@app.get("/leads/", response_model=list)
def read_leads(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    leads = db.query(Lead).offset(skip).limit(limit).all()
    db.close()
    return [{"id": lead.id, "prospect_id": lead.prospect_id, "messages": lead.messages, "notes": lead.notes, "status": lead.status.value} for lead in leads]