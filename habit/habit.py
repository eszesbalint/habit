from flask import render_template
from datetime import date as d, timedelta as td
from sqlalchemy.orm import reconstructor

from habit import db
from habit.month import Month as m

_week_days = [d(2001, 1, i+1).strftime("%a") for i in range(7)]

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(16), nullable=False, default="black")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    data_blocks = db.relationship("DataBlock", backref="habit", lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(Habit, self).__init__(*args, **kwargs)
        self._frequency = None
        self._pattern = None
        self._first = None
        self._last = None

    @reconstructor
    def init_on_load(self):
        self._frequency = None
        self._pattern = None
        self._first = None
        self._last = None
        self._update_stats()

    def predict(self, date=None):
        if self.empty:
            return False
        elif date > self._last and self._pattern:
            return self._pattern[(date-self._last).days % len(self._pattern)]
        else:
            return False

    def _update_stats(self):
        # If the habit has occurred at least once
        if not self.empty:
            # Find first date
            first_block = self.data_blocks.order_by(
                DataBlock.year.asc(),
                DataBlock.month.asc()
                ).first()
            if first_block:
                year, month = first_block.year, first_block.month
                first_date = None
                for date in m(year, month).dates:
                    if self[date]:
                        first_date = date
                        break
                self._first = first_date
            
            # Find last date
            last_block = self.data_blocks.order_by(
                DataBlock.year.desc(),
                DataBlock.month.desc()
                ).first()
            if last_block:
                year, month = last_block.year, last_block.month
                last_date = None
                for date in reversed(m(year, month).dates):
                    if self[date]:
                        last_date = date
                        break
                self._last = last_date

            # If there's at least 7 days between the first and the last
            # occurrence
            if (self._last - self._first).days > 7:
                # Calculate habit frequency
                last_28 = self[
                    max(self._last-td(8*7-1),self._first) : self._last+td(1)
                    ]
                scores = [
                    sum([
                        int(a&b)
                        for a, b in zip(last_28+[0]*i,[0]*i+last_28)
                    ])/(len(last_28)-i*.5)
                    for i in range(1,len(last_28)//2+1)
                ]
                self._frequency = scores.index(max(scores)) + 1
                # Extract pattern
                self._pattern = self[self._last-td(self._frequency):self._last]

    @property
    def empty(self):
        return not self.data_blocks.all()


    def __getitem__(self, key):
        if isinstance(key, d) or isinstance(key, m):
            block = self.data_blocks.filter_by(year=key.year, month=key.month).first()
            if block:
                return block[key]
            else:
                return False
        elif isinstance(key, slice):
            if isinstance(key.start, d) and isinstance(key.stop, d):
                return [self[key.start + td(day)] 
                        for day in range((key.stop-key.start).days)
                        ]
            else:
                raise KeyError("")
        else:
            raise KeyError("")

    def __setitem__(self, key, value):
        block = self.data_blocks.filter_by(year=key.year, month=key.month).first()
        if not block:
            block = DataBlock(year=key.year, month=key.month, habit_id=self.id)
            db.session.add(block)
            db.session.commit()
        block[key] = value
        if not block.data:
            DataBlock.query.filter_by(id=block.id).delete()
            db.session.commit()


    def render(self, month):
        self._update_stats()
        return  render_template(
            "calendar.html", 
            habit = self,
            month=month,
            week_days=_week_days,
            )

    
class DataBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False, default=1)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    data = db.Column(db.Integer, default=0)

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
    