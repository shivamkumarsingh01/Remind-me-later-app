from datetime import time, timedelta
from app.models.reminder import Reminder
from app.database import get_db_connection

def convert_mysql_time(time_value):
    """Convert MySQL time/timedelta to Python time object"""
    if isinstance(time_value, timedelta):
        
        total_seconds = time_value.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return time(hour=hours, minute=minutes, second=seconds)
    elif isinstance(time_value, str):
        
        try:
            hours, minutes, seconds = map(int, time_value.split(':'))
            return time(hour=hours, minute=minutes, second=seconds)
        except ValueError:
            pass
    return time(0, 0)  

def create_reminder(reminder_data: dict) -> Reminder:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
    INSERT INTO reminders 
    (message, reminder_date, reminder_time, notification_method) 
    VALUES (%s, %s, %s, %s)
    """
    
    values = (
        reminder_data['message'],
        reminder_data['reminder_date'],
        reminder_data['reminder_time'].strftime('%H:%M:%S'),
        reminder_data['notification_method']
    )
    
    cursor.execute(query, values)
    connection.commit()
    
    # Get the inserted record
    reminder_id = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return get_reminder(reminder_id)

def get_reminder(reminder_id: int) -> Reminder:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM reminders WHERE id = %s", (reminder_id,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if result:
        # Convert MySQL time to Python time object
        result['reminder_time'] = convert_mysql_time(result['reminder_time'])
        
        return Reminder(
            id=result['id'],
            message=result['message'],
            reminder_date=result['reminder_date'],
            reminder_time=result['reminder_time'],
            notification_method=result['notification_method'],
            is_sent=result['is_sent']
        )
    return None

def get_all_reminders() -> list[Reminder]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM reminders")
    results = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    reminders = []
    for result in results:
        # Convert MySQL time to Python time object
        result['reminder_time'] = convert_mysql_time(result['reminder_time'])
        
        reminders.append(Reminder(
            id=result['id'],
            message=result['message'],
            reminder_date=result['reminder_date'],
            reminder_time=result['reminder_time'],
            notification_method=result['notification_method'],
            is_sent=result['is_sent']
        ))
    
    return reminders