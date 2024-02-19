from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField, SubmitField, TextAreaField, PasswordField, SelectField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from datetime import date

class AgeValidator:
    def __init__(self, min_age=7, max_age=90, message=None):
        self.min_age = min_age
        self.max_age = max_age
        if not message:
            message = f'Age must be between {min_age} and {max_age}.'
        self.message = message

    def __call__(self, form, field):
        try:
            birthdate = field.data
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < self.min_age or age > self.max_age:
                raise ValidationError(self.message)
        except (ValueError, TypeError):
            raise ValidationError('Invalid date format.')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Invalid name")], render_kw={"placeholder": "Иван"})
    # surname = StringField('Surname', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Invalid surname")], render_kw={"placeholder": "Иванов"})
    # patronymic = StringField('Surname', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Invalid patronymic")], render_kw={"placeholder": "Иванович"}) # отчество
    # gender = RadioField('Gender', choices=[('М','М'), ('Ж','Ж')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', message="Invalid email")], render_kw={"placeholder": "ivanov@mail.ru"})
    password = PasswordField('Password', validators=[DataRequired()])
    # city = StringField('City', validators=[DataRequired(), Regexp('^[а-яА-ЯёЁa-zA-Z]+$', message="Invalid city")], render_kw={"placeholder": "Иваново"})
    telephone = StringField('Telephone', validators=[DataRequired(), Regexp('^\d{10}$', message="Invalid phone number")], render_kw={"placeholder": "71234567890"})
    # birthday = DateField('Birthday', validators=[DataRequired(), AgeValidator()])
    # vk = StringField('VK', validators=[DataRequired(), Regexp('(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/\S*)?', message="Invalid link")])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CompetitionForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    image = FileField('Картинка', validators=[DataRequired()])
    date = DateField('Дата', validators=[DataRequired()])
    submit = SubmitField('Добавить')

