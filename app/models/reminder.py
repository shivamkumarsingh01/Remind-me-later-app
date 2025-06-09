from datetime import date, time
from typing import Literal

NotificationMethod = Literal['SMS', 'EMAIL']

class Reminder:
    def __init__(
        self,
        message: str,
        reminder_date: date,
        reminder_time: time,
        notification_method: NotificationMethod,
        id: int = None,
        is_sent: bool = False
    ):
        self.id = id
        self.message = message
        self.reminder_date = reminder_date
        self.reminder_time = reminder_time
        self.notification_method = notification_method
        self.is_sent = is_sent