import pandas as pd
import time
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, jsonify, session, Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from forms import RegistrationForm, LoginForm, CompetitionForm, AddUserForm,  fields_reg
from configs_clases import User, Competition, UserAdd, app, db, login_manager

# Контекстный процессор для передачи формы входа во все шаблоны
@app.context_processor
def inject_login_form():
    return dict(login_form=LoginForm())
def inject_registration_form():
    return dict(registration_form=RegistrationForm())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit(): # проверка на валидацию       
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        telephone = request.form['telephone']
        birthday = request.form['birthday']
        vk = request.form['vk']
        
        # Хешируем пароль перед сохранением в базу данных
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, surname=surname, patronymic=patronymic, gender=gender, 
                        email=email, password=hashed_password, city=city, telephone=telephone, 
                        birthday=birthday, vk=vk)
        db.session.add(new_user)
        db.session.commit()
        # Автоматическая авторизация после успешной регистрации
        login_user(new_user)

        return redirect(url_for('profile'))

    return render_template('register.html', form=registration_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form['email']
        # password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        user = User.query.filter_by(email=email).first()
        # if user and user.password == password:
        login_user(user)
        if user.email == 'admin@list.ru':
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('profile'))

    return render_template('login.html', form=login_form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Получаем список пользователей, добавленных текущим пользователем
    current_user_id = current_user.id
    added_users = UserAdd.query.join(User, User.id == UserAdd.user_id).all()
  
    return render_template('profile.html', users=added_users, current_user_id=current_user_id) #, form_added_users=form_added_users, added_users=added_users, user=current_user, users=users, added_users=added_users) #user_data=user_data, form=RegistrationForm(), 

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user = User.query.get(current_user.id)
    form = RegistrationForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile_edit.html', form=form)

@app.route('/profile/add_user', methods=['GET', 'POST'])
@login_required
def profile_add_user():
    form = AddUserForm()
    if form.validate_on_submit(): # проверка на валидацию       
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        gender = request.form['gender']       
        city = request.form['city']
        birthday = request.form['birthday']
        
        new_add_user = UserAdd(user_id = current_user.id, name=name, surname=surname, patronymic=patronymic, gender=gender, city=city, birthday=birthday)
        db.session.add(new_add_user)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('profile_add_user.html', form=form)

@app.route('/profile/edit_add', methods=['GET', 'POST'])
@login_required
def profile_edit_add():
    user_add = User.query.get(current_user.id)
    form = AddUserForm(obj=user_add)
    if form.validate_on_submit():
        form.populate_obj(user_add)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('profile_edit_add.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    competitions = Competition.query.all()
    return render_template('index.html', competitions=competitions)#, form = form)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/add_competition', methods=['GET', 'POST'])
def add_competition():
    form = CompetitionForm()
    if form.validate_on_submit():
        competition = Competition(title=form.title.data, date=form.date.data)
        if form.image.data:
            filename = form.image.data.filename
            form.image.data.save(os.path.join('static', 'images', 'competitions', filename))
            competition.image = filename
        db.session.add(competition)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_competition.html', form=form)

with app.app_context(): 
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)