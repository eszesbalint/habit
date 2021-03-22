from habit import db, login_manager
from flask_login import UserMixin
import datetime

from habit.habit import Habit

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    habits = db.relationship("Habit", backref="owner", lazy="dynamic")
    _date = datetime.date.today()
    def __repr__(self):
        return f"User({self.id}, {self.email})"

    def new_habit(self, *args, **kwargs):
        habit = Habit(*args, **kwargs, user_id=self.id)
        db.session.add(habit)
        db.session.commit()

    def delete_habit(self, habit_id):
        habit = self.habits.filter_by(id=habit_id).first()
        if habit:
            habit.data_blocks.delete()
            self.habits.filter_by(id=habit_id).delete()
            db.session.commit()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def render_habits(self):
        pass