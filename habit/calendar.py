from flask import render_template
from datetime import date as d, timedelta as td

from habit import db
from habit.month import Month

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(16), nullable=False, default="black")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    calendars = db.relationship("Calendar", backref="habit", lazy="dynamic")

    def get_calendar(self, month):
        calendar = self.calendars.filter_by(year=month.year, month=month.month).first()
        if calendar:
            return calendar
        else:
            calendar = Calendar(year=month.year, month=month.month, habit_id=self.id)
            db.session.add(calendar)
            db.session.commit()
            return calendar

    
class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False, default=1)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    data = db.Column(db.Integer, default=0)

    def render(self):
        f = Month(self.year, self.month)
        self.dates = f.dates
        self.week_days = [d(2001, 1, i+1).strftime("%a") for i in range(7)]
        self.offset=f.weekday()
        return render_template("calendar.html", calendar = self)

    def __getitem__(self, date):
        if date.year == self.year and date.month == self.month:
            data = self.data
            position = date.day - 1
            return bool(data >> position & 1)

    def __setitem__(self, date, value):
        if date.year == self.year and date.month == self.month:
            data = self.data
            value = bool(value)
            if not (value and self[date]):
                position = date.day - 1
                self.data = data ^ (2**position)
                db.session.commit()
    