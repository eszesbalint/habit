from datetime import date as d
from flask_login import current_user
from habit import socketio
from flask_socketio import send, emit

from habit.calendar import Habit, Calendar

@socketio.on("user_connected")
def update_user_date(data):
    year, month, day = data["user_date"]
    date = d(year, month, day)
    current_user.date = date

@socketio.on("date_toggled")
def check_clear(data):
    calendar = Calendar.query.filter_by(id=int(data["calendar_id"])).first()
    if calendar:
        date = d(calendar.year, calendar.month, int(data["day"]))
        calendar[date] = not calendar[date]
        
    
