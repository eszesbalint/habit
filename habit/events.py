from datetime import date as d
from flask_login import current_user
from habit import socketio
from flask_socketio import send, emit

from habit.habit import Habit
from habit.month import Month as m

@socketio.on("user_connected")
def update_user_date(data):
    year, month, day = data["user_date"]
    date = d(year, month, day)
    current_user.date = date

@socketio.on("date_toggled")
def toggle_date(data):
    habit = Habit.query.filter_by(id=data["habit_id"]).first()
    if habit:
        if habit.owner == current_user:
            year, month, day = data["date"]
            date = d(year, month, day)
            habit[date] = not habit[date]
            habit.predict()

@socketio.on("month_changed")
def render_habits(data):
    year, month = data["month"]
    month = m(year, month)
    rendered = ''.join([
        habit.render(month) for habit in current_user.habits.all()
        ])
    socketio.emit(
        "habits_rendered",
        {
            "HTML" : rendered
        }
        )
    
    
