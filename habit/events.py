from datetime import date as D
from flask_login import current_user
from habit import socketio
from flask_socketio import send, emit
from flask import render_template

from habit.habit import Habit
from habit.month import Month as M


@socketio.on("user_connected")
def update_user_date(data):
    current_user.stats.date = D(*data["user_date"])


@socketio.on("date_toggled")
def toggle_date(data):
    hs, d = (current_user.habits, D(*data["date"]))
    h = hs.filter_by(id=data["habit_id"]).first()
    if h:
        h[d] = not h[d]


@socketio.on("habit_changed")
def render_habit(data):
    hs, m = (current_user.habits, M(*data["month"]))
    h = hs.filter_by(id=data["habit_id"]).first()
    if h:
        socketio.emit("habit_rendered",{"habit_id": h.id, "HTML":h.render(m)})


@socketio.on("month_changed")
def render_habits(data):
    m, d = (M(*data["month"]), data["direction"])
    m = m.next() if d == "forwards" else m.previous()
    print(m)
    mhtml = render_template("month.html", month=m)
    hhtml = current_user.render_habits(m)
    socketio.emit(
        "month_rendered",
        {
            "month":{"HTML":mhtml},
            "habits":{"HTML":hhtml},
            "direction":d
            }
        )
    
    
