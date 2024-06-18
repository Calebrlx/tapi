from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import random
import pyautogui
import time

DATABASE_URL = "mysql+mysqlconnector://root:abghse@db/sales_system"

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
    messages = Column(JSON, nullable=False)
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
    messages: list[dict]
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

@app.post("/send-message/", response_model=dict)
def send_message(slug: str):
    db = SessionLocal()
    db_prospect = db.query(Prospect).filter(Prospect.slug == slug).first()
    if db_prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")

    # Logic to determine the message
    if db_prospect.status == ProspectStatus.not_contacted:
        message = random.choice(greetings)
        db_prospect.status = ProspectStatus.contacted
    elif db_prospect.status == ProspectStatus.contacted:
        message = random.choice(follow_up)
        db_prospect.status = ProspectStatus.followed_up
    elif db_prospect.status == ProspectStatus.followed_up:
        message = "No more follow-ups."
        db_prospect.status = ProspectStatus.unresponsive
    else:
        message = "This prospect is marked as unresponsive."

    # Send the message using pyautogui
    automate_task(slug, message)

    # Update prospect contact count
    db_prospect.contact_count += 1
    db.commit()
    db.refresh(db_prospect)
    db.close()
    
    return {"id": db_prospect.id, "slug": db_prospect.slug, "message": message}

def automate_task(slug, msg):
    # Replace the coordinates and actions with those specific to your setup
    pyautogui.moveTo(300, 300, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(670, 130, duration=0.5)
    pyautogui.click()
    pyautogui.typewrite(slug, interval=0.1)
    pyautogui.press('enter')
    pyautogui.typewrite(msg, interval=0.1)
    pyautogui.press('enter')
    time.sleep(2)  # Adjust sleep time as needed

# Example initial messages and follow-ups
greetings = [
    "Hey there! How are you doing today?",
    "Hi! Hope you’re having a great day!",
    "Hello! How’s it going?",
    "Hi! How are things with you?",
    "Hey! How’s your day been?",
    "Good morning! How are you?",
    "Hi there! How are things on your end?",
    "Hello! What’s up?",
    "Hey! How’s your day treating you?",
    "Hi! How’s everything going?",
    "Good afternoon! How have you been?",
    "Hello! How’s it going for you today?",
    "Hi! How’s your day shaping up?",
    "Hey there! How’s your day been so far?",
    "Hi! Hope your day is going well!",
    "Hello! How’s everything with you?",
    "Hi! How are you feeling today?",
    "Hey! How have you been?",
    "Hello! How’s your day progressing?",
    "Hi! How’s it going for you?"
]

follow_up = [
    "Hi again! Just wanted to introduce myself properly. I’m Peyton Hassan, an indie artist, and I create unique die-cut stickers. Would you be interested in checking them out?",
    "Hey! Following up from yesterday. I wanted to share that I design fun and whimsical die-cut stickers. Let me know if you’d like to see them!",
    "Hello again! I realized I didn’t mention this yesterday—I’m an indie artist and I make custom die-cut stickers. Would you like to see some of my designs?",
    "Hi there! I forgot to tell you yesterday that I create unique die-cut stickers. Are you interested in seeing some of my work?",
    "Hey! Just wanted to let you know that I design original die-cut stickers. If you’re interested, I’d love to share some of my designs with you."
]