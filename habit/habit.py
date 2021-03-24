from flask import render_template
from datetime import date as D, timedelta as TD
from sqlalchemy.orm import reconstructor

from habit import db
from habit.month import Month as M


_week_days = [D(2001, 1, i+1).strftime("%a") for i in range(7)]


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(16), nullable=False, default="black")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    data_blocks = db.relationship("DataBlock", backref="habit", lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(Habit, self).__init__(*args, **kwargs)
        self._init_stats()

    @reconstructor
    def _init_stats(self):
        self.stats = HabitStats(self)

    def __getitem__(self, key):
        k, dbs, inst = (key, self.data_blocks, isinstance)
        if inst(k, D) or inst(k, M):
            b = dbs.filter_by(year=key.year, month=key.month).first()
            return b[k] if b else False
        elif inst(k, slice):
            f, l = (k.start, k.stop)
            if inst(f, D) and inst(l, D):
                return [self[f+TD(d)] for d in range((l-f).days)]

    def __setitem__(self, key, value):
        k, v, dbs, DB = (key, value, self.data_blocks, DataBlock)
        b = dbs.filter_by(year=k.year, month=k.month).first()
        if not b and v:
            b = DB(year=k.year, month=k.month, habit_id=self.id)
            db.session.add(b)
            db.session.commit()
        if b:
            b[k] = v
        if b and not b.data:
            DB.query.filter_by(id=b.id).delete()
            db.session.commit()


    def render(self, month):
        self.stats.update()
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

    @property
    def dates(self):
        return M(self.year, self.month).dates

    def __getitem__(self, date):
        if date in self.dates:
            return bool(self.data >> (date.day-1) & 1)

    def __setitem__(self, date, value):
        if date.year == self.year and date.month == self.month:
            data = self.data
            value = bool(value)
            if not (value and self[date]):
                position = date.day - 1
                self.data = data ^ (2**position)
                db.session.commit()
    

class HabitStats():
    def __init__(self, habit):
        self.habit = habit
        self.pattern, self.first, self.last = (None, None, None)

    def update(self):
        self.first, self.last = self._calc_first_last()
        self.pattern = self._calc_pattern()

    def predict(self, date=None):
        d, l, p = (date, self.last, self.pattern)
        return p[(d-l).days % len(p)] if p and l and d > l else False

    def _calc_first_last(self):
        h, DB, rev = (self.habit, DataBlock, reversed)
        fb = h.data_blocks.order_by(DB.year.asc(), DB.month.asc()).first()
        lb = h.data_blocks.order_by(DB.year.desc(), DB.month.desc()).first()
        return (next((d for d in fb.dates if fb[d]), None),
                next((d for d in rev(lb.dates) if lb[d]), None)) \
                if fb and lb else (None, None)

    def _calc_pattern(self):
        f, l, h = (self.first, self.last, self.habit)
        if f == l:
            return None
        elif (l-f).days > 7:
            tw = h[max(l-TD(8*7-1),f) : l+TD(1)] # Time window
            # Auto correlating time window
            s = [
                sum([int(a&b) for a, b in zip(tw+[0]*i,[0]*i+tw)])
                /(len(tw)-i*.5)
                for i in range(1,len(tw)//2+1)
            ]
            # Finding the most fitting frequency
            fq = s.index(max(s)) + 1
            # Pattern is the last frequency lenth sequence of the habit
            return h[l-TD(fq):l] 