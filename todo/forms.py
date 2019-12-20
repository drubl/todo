from django.forms import Form, CharField, HiddenInput, Textarea, PasswordInput, BooleanField, HiddenInput, ValidationError, ModelChoiceField

from .models import Category

class LoginForm(Form):
    username = CharField(max_length=50, label="Имя пользователя")
    password = CharField(widget=PasswordInput, label="Пароль")
    remember_me = BooleanField(required=False, label="Запомнить меня")

class RegisterForm(Form):
    username = CharField(max_length=50, min_length=5, label="Имя пользователя")
    password1 = CharField(widget=PasswordInput, label="Пароль")
    password2 = CharField(widget=PasswordInput, label="Повторите пароль", validators=())

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get('password1')
    #     password2 = cleaned_data.get('password2')
        
    #     if password1 != password2:
    #         raise ValidationError("Пароли не совпадают")


class AddTaskForm(Form):
    title = CharField(max_length=50, label='Задача')
    body = CharField(widget=Textarea, label='Описание')
    category = ModelChoiceField(queryset=None, label='Категория', required=False, empty_label="----------")

class DeleteTaskForm(Form):
    task_id = CharField(widget=HiddenInput)

class CompliteTaskForm(Form):
    task_id = CharField(widget=HiddenInput) #todo: Соединить в одну форму
    