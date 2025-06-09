from fastapi import FastAPI, HTTPException
from datetime import time
from typing import List
from app.schemas.reminder import ReminderCreate, Reminder
from app.crud.reminder import create_reminder, get_reminder, get_all_reminders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/reminders/", response_model=Reminder)
async def create_reminder_endpoint(reminder: ReminderCreate):
    try:
       
        reminder_data = reminder.model_dump()
        
        
        created_reminder = create_reminder(reminder_data)
        
        if not created_reminder:
            raise HTTPException(status_code=500, detail="Failed to create reminder")
            
        return created_reminder
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reminders/{reminder_id}", response_model=Reminder)
async def read_reminder(reminder_id: int):
    reminder = get_reminder(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@app.get("/reminders/", response_model=List[Reminder])
async def list_reminders():
    return get_all_reminders()

@app.get("/")
async def root():
    return {"message": "Remind-me-later API is running"}