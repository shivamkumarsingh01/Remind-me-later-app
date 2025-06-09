from datetime import time, date
from typing import Literal
from pydantic import BaseModel, field_validator

NotificationMethod = Literal['SMS', 'EMAIL']

class ReminderCreate(BaseModel):
    message: str
    reminder_date: date
    reminder_time: time  # Using time instead of str
    notification_method: NotificationMethod

    @field_validator('reminder_time')
    def validate_time(cls, v):
        if isinstance(v, str):
            try:
                hours, minutes, seconds = map(int, v.split(':'))
                return time(hour=hours, minute=minutes, second=seconds)
            except ValueError:
                raise ValueError("Time must be in HH:MM:SS format")
        return v

class Reminder(ReminderCreate):
    id: int
    is_sent: bool = False

    class Config:
        from_attributes = True