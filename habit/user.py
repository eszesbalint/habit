from habit import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import reconstructor
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
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._init_stats()

    @reconstructor
    def _init_stats(self):
        self.stats = UserStats(self)

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

    def render_habits(self, month):
        hs, m = (self.habits, month)
        return ''.join([h.render(m) for h in hs.all()])


class UserStats():
    def __init__(self, user):
        self.user = user
        self.date = datetime.date.today()