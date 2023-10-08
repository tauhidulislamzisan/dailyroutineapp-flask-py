from app import app, db, User, Routine

# from app.app import User,Log
from flask import render_template, request, redirect, url_for, flash
from app.forms import LoginForm, SettingForm, InfoForm, RegistrationForm, AddRoutineForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from datetime import datetime

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()  
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(
            generate_password_hash(user.password), form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("The user name and password do not match", "danger")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()  

    if form.validate_on_submit():
        
        hashed_password = form.password.data
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
  
    form = SettingForm()
    if form.validate_on_submit():
        if check_password_hash(
            generate_password_hash(current_user.password), form.password.data
        ):
            user = User.query.filter_by(id=current_user.id).first()
            new_password = form.new_password.data
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash("Successfully modified", "success")
            return redirect(url_for("account"))
        else:
            flash("Wrong original password", "danger")
    return render_template("account.html", form=form)


@app.route("/")
@login_required
def indexH():
    return redirect(url_for("index"))
@app.route("/info")
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("info.html", user=user) 


@app.route("/edit")
@login_required
def edit():
    form = InfoForm()
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("edit.html", user=user, form=form)


@app.route("/update", methods=["POST"])
@login_required
def update():
    form = InfoForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.username   = request.form['username']
        try:
            db.session.commit()
        except:
            db.session.rollback() 
        flash('Successfully modified', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html',form=form,user=user)



@app.route("/lists",methods=["GET","POST"])
@login_required
def lists():
    form = AddRoutineForm()  
    if form.validate_on_submit():
        routine = Routine(
            user_id=current_user.id,
            details=form.details.data,
            done=False,
            update_time=datetime.now(),
        )
        db.session.add(routine)
        db.session.commit()
        flash("Routine added successfully.", "success")
    Routines = Routine.query.filter_by(user_id=current_user.id).all()
    return render_template("list.html", data=Routines,form=form)
@app.route("/update_status/<int:id>/type/<type>")
@login_required
def update_status(id, type):
    routine = Routine.query.filter_by(id=id).first()
    if type == "complete":
        routine.done = 1
        routine.update_time=datetime.now()
        db.session.commit()
        return redirect(url_for("lists"))
    elif type == "incomplete":
        routine.done = 0
        routine.update_time=datetime.now()
        db.session.commit()
        return redirect(url_for("lists"))
    elif type == "delete":
        if routine:
            db.session.delete(routine)
            db.session.commit()
            flash('Routine deleted successfully.', 'danger')
            return redirect(url_for("lists"))
    return render_template("404.html"), 404

@app.errorhandler(404)
def page_note_found(e):
    return render_template("404.html"), 404
