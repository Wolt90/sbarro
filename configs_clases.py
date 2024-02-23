from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField

# Модель админа
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == 'admin@list.ru'

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and current_user.email == 'admin@list.ru':
            return self.render('admin_home.html')
        else:
            return redirect(url_for('profile'))
    
app = Flask(__name__)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
db1, db2 = "sqlite:///users.db", 'sqlite:///competitions.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db1
# app.config['SQLALCHEMY_DATABASE_URI_2'] = db2
app.config['SQLALCHEMY_BINDS'] = {'db1': db1,'db2': db2}
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель для хранения пользователей
class User(UserMixin, db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    patronymic = db.Column(db.String(50), unique=False, nullable=True) # отчество
    gender = db.Column(db.String(1), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    telephone = db.Column(db.String(50), unique=True, nullable=False)
    birthday = db.Column(db.String(50), unique=False, nullable=False)
    vk = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name
    
class Competition(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    date = db.Column(db.Date, nullable=False)

# Определение представления для модели
class CompetitionView(ModelView):
    # Добавление поля для загрузки изображения
    form_extra_fields = {
        'image': ImageUploadField('Image', base_path='static/images/competitions', url_relative_path='uploads/competitions/')
    }

admin.add_view(ModelView(User, db.session))
admin.add_view(CompetitionView(Competition, db.session))