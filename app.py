import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

# Модель для хранения пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    # image = 
    date = TextAreaField('Дата', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    # Генерируем данные для таблицы
    data = [
        ['Value 1', 'Value 2', 'Value 3'],
        ['Value 4', 'Value 5', 'Value 6'],
        ['Value 7', 'Value 8', 'Value 9']
    ]
    return render_template('page1.html', data=data)

# Другие маршруты для остальных страниц

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/page5')
def page5():
    return render_template('page5.html')

@app.route('/page6')
def page6():
    return render_template('page6.html')

with app.app_context(): 
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)