from datetime import date as d, timedelta as td
from flask import render_template, redirect, url_for
from flask_login import (current_user, login_required, 
                        login_user, logout_user)

from habit import app, db, bcrypt
from habit.user import User
from habit.forms import RegisterForm, LoginForm, HabitForm
from habit.calendar import Habit, Calendar
import habit.events
from habit.month import Month as m


@app.route("/", defaults={"year":d.today().year, 
                          "month":d.today().month})
@app.route("/<int:year>/<int:month>")
@login_required
def tracker(year, month):
    month = m(year, month)
    return render_template(
        "tracker.html", 
        month=month,
        next_month=month.next(),
        previous_month=month.previous()
        )


@app.route("/edit/<int:habit_id>", methods=["GET", "POST"])
def edit(habit_id=None):
    form = HabitForm()
    habit = Habit.query.filter_by(id=habit_id).first()
    if habit and habit.owner == current_user:
        if form.validate_on_submit():
            habit.name = form.name.data
            habit.color = form.color.data
            db.session.commit()
            return redirect(url_for("tracker"))

        return render_template("habit.html", habit=habit, form=form)


@app.route("/new", methods=["GET", "POST"])
def new():
    form = HabitForm()
    if form.validate_on_submit():
        current_user.new_habit(
            name=form.name.data,
            color=form.color.data
            )
        return redirect(url_for("tracker"))

    return render_template("habit.html", form=form)

@app.route("/delete/<int:habit_id>", methods=["GET", "POST"])
def delete(habit_id=None):
    Habit.query.filter_by(id=habit_id).delete()
    Calendar.query.filter_by(habit_id=habit_id).delete()
    db.session.commit()
    return redirect(url_for("tracker"))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        e = register_form.email.data
        p = register_form.password.data
        h = bcrypt.generate_password_hash(p)
        h = h.decode("utf-8")
        new_user = User(email=e, password=h)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    if login_form.validate_on_submit():
        e = login_form.email.data
        p = login_form.password.data
        u = User.query.filter_by(email=e).first()
        h = u.password
        if u and bcrypt.check_password_hash(h,p):
            login_user(u)
            return redirect(url_for("tracker"))

    return render_template(
        "login.html", 
        login_form=login_form,
        register_form=register_form
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("tracker"))