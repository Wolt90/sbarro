from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField, SubmitField, TextAreaField, PasswordField, SelectField, RadioField, widgets, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from configs_clases import User

class AgeValidator:
    def __init__(self, min_age=7, max_age=90, message=None):
        self.min_age = min_age
        self.max_age = max_age
        if not message:
            message = f'Возраст должен быть между {min_age} и {max_age}.'
        self.message = message

    def __call__(self, form, field):
        try:
            birthdate = field.data
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < self.min_age or age > self.max_age:
                raise ValidationError(self.message)
        except (ValueError, TypeError):
            raise ValidationError(f'Ошибка, возраст только от {self.min_age} до {self.max_age}')
    
class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Введите только буквы")], render_kw={"placeholder": "Иван"})
    surname = StringField('Фамилия', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Введите только буквы")], render_kw={"placeholder": "Иванов"})
    patronymic = StringField('Отчество', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Введите только буквы")], render_kw={"placeholder": "Иванович"}) # отчество
    gender = RadioField('Пол', choices=[('М','М'), ('Ж','Ж')], validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Regexp('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', message="Не почта, пример - ivanov@mail.ru")], render_kw={"placeholder": "ivanov@mail.ru"})   #Email(), 
    password = PasswordField('Пароль', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Введите только буквы")], render_kw={"placeholder": "Иваново"})
    telephone = StringField('Телефон', validators=[DataRequired(), Regexp('^\d{11}$', message="Введите 11 цифр без () и +, пример 79102345678")], render_kw={"placeholder": "79102345678"})
    birthday = DateField('День рождения', validators=[DataRequired(), AgeValidator()])
    vk = StringField('Ссылка на вконтакте', validators=[DataRequired(), Regexp('(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/\S*)?', message="Ошибка, пример ссылки: https://vk.com/example")], render_kw={"placeholder": "https://vk.com/example"})
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Пользователь существует. Пожалуйста, <a href="/login">авторизуйтесь</a> или измените почту')

class EditProfileForm(RegistrationForm):
    submit = SubmitField('Сохранить изменения')
    pass

class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])   #Email(), 
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('Пользователь не найден. Пожалуйста, зарегистрируйтесь или введите корректную почту')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                raise ValidationError('Неверный пароль')

class CompetitionForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    image = FileField('Картинка', validators=[DataRequired()])
    date = DateField('Дата', validators=[DataRequired()])
    submit = SubmitField('Добавить')

