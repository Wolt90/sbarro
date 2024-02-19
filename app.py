import pandas as pd
import time
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from forms import RegistrationForm, LoginForm, CompetitionForm
from configs_clases import User, Competition, app, db, login_manager

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
        
        # if request.method == 'POST':
        name = request.form['name']
        # surname = request.form['surname']
        # patronymic = request.form['patronymic']
        # gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        # city = request.form['city']
        telephone = request.form['telephone']
        # birthday = request.form['birthday']
        # vk = request.form['vk']
    
    # Проверяем, существует ли пользователь с таким же именем
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            # return redirect(url_for('register'))
        
        # Хешируем пароль перед сохранением в базу данных
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, 
                        email=email, password=hashed_password, telephone=telephone) 
                        # birthday=birthday, vk=vk)
        # new_user = User(name=name, surname=surname, patronymic=patronymic, gender=gender, 
        #                 email=email, password=hashed_password, city=city, telephone=telephone, 
        #                 birthday=birthday, vk=vk)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Пожалуйста, войдите', 'success')
    else: 
        flash('Ошибка', 'error')
        # return redirect(url_for('register'))

    return render_template('register.html', registration_form=registration_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Ищем пользователя в базе данных
        email = User.query.filter_by(email=email).first()
        if email:
            # Проверяем, соответствует ли введенный пароль хэшу в базе данных
            if check_password_hash(email.password, password):
                session['email'] = email
                flash('Вы успешно вошли', 'success')
                return redirect(url_for('profile'))
        
        flash('Неправильное имя пользователя или пароль', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        return render_template('profile.html', username=session['email'])
    else:
        flash('Пожалуйста, войдите, чтобы получить доступ к профилю', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Вы успешно вышли', 'success')
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
            form.image.data.save(os.path.join('static', 'images', filename))
            competition.image = filename
        db.session.add(competition)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_competition.html', form=form)

with app.app_context(): 
    db.create_all() 

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)