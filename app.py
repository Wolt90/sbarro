import pandas as pd
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, FileField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///competitions.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

# Модель для хранения пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверяем, что пользователь с таким именем еще не зарегистрирован
        if User.query.filter_by(username=username).first():
            # print('Пользователь с таким именем уже зарегистрирован!')
            # time.sleep(2)
            return 'Пользователь с таким именем уже зарегистрирован!' #redirect('/register')

        # Добавляем нового пользователя в базу данных
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/success')
    return render_template('register.html')

@app.route('/success')
def success():
    # print('Регистрация прошла успешно!')
    # time.sleep(5)
    return 'Регистрация прошла успешно!' #redirect('/')

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    date = db.Column(db.Date, nullable=False)

class CompetitionForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    image = FileField('Картинка', validators=[DataRequired()])
    date = DateField('Дата', validators=[DataRequired()])
    submit = SubmitField('Добавить')

@app.route('/')
def index():
    competitions = Competition.query.all()
    return render_template('index.html', competitions=competitions)

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