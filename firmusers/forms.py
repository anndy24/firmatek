from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import inlineformset_factory

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['image', 'title', 'street', 'description', 'start_date', 'end_date', 'is_active', 'professions', 'files', 'open']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', "class": "form-control"}),
            'end_date': forms.DateInput(attrs={'type': 'date', "class": "form-control"}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'professions': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'files': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
            'open': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image': 'Изображение',
            'title': 'Название',
            'street': 'Улица',
            'description': 'Описание',
            'start_date': 'Дата начала',
            'end_date': 'Дата завершения',
            'is_active': 'Активность', 
            'professions': 'Подрядчики',
            'files': 'Файл',
            'open': 'Открытый доступ'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name', 'start_date', 'end_date','is_done']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'type': 'date','class': 'form-control'}),
            'end_date': forms.TextInput(attrs={'type': 'date','class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'project': 'Проект',
            'name': 'Задача',
            'start_date': 'Дата начала',
            'end_date': 'Дата завершения',
            'is_done': 'Выполнена',         
        }


class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['task', 'name', 'start_date', 'end_date','is_done']
        labels = {
            'name': 'Подзадача',
            'start_date': 'Дата начала',
            'end_date': 'Дата завершения',
            'is_done': 'Выполнена',    
        }
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

SubtaskFormSet = inlineformset_factory(Task, Subtask, fields=['name', 'start_date', 'end_date','is_done'], extra=3, can_delete=False, widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }, labels = {
            'name': 'Подзадача',
            'start_date': 'Дата начала',
            'end_date': 'Дата завершения',
            'is_done': 'Выполнена',    
        }) 

class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ('name',)
        labels = {
            'name': 'Подрядчик',     
        } 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FirmuserForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    number = forms.CharField(
        label='Номер автомобиля',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Firmuser
        fields = ['first_name', 'last_name', 'professions', 'email', 'phone', 'number', 'username', 'password']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'professions': 'Подрядчик',
            'email': 'Email',
            'phone': 'Телефон',
            'number': 'Номер автомобиля',
            'password': 'Пароль',
            
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'professions': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            
    def save(self, commit=True):
        user = super(FirmuserForm, self).save(commit=False)
        phone_number = self.cleaned_data['phone']
        if commit:
            user.save()
            Phone.objects.create(user=user, name=phone_number)
        return user

class SignUpForm(UserCreationForm):
    phone = forms.CharField(
        label='',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Телефон"}),
    )
    number = forms.CharField(
        label='',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Номер машины"}),
    )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data['phone']
        car_number = self.cleaned_data['number']
        if commit:
            user.save()
            Phone.objects.create(user=user, name=phone_number)
            CarNumber.objects.create(user=user, number=car_number)
        return user

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Фамилия"}
        ),
    )

    class Meta:
        model = Firmuser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Логин"
        self.fields["username"].label = ""
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Обязательно. 150 символов или меньше. Только буквы, цифры и @/./+/-/_.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Пароль"
        self.fields["password1"].label = ""
        self.fields[
            "password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Ваш пароль не должен быть слишком похож на другую личную информацию.</li><li>Ваш пароль должен содержать не менее 8 символов.</li><li>Ваш пароль не должен быть широко используемым паролем.</li><li>Ваш пароль не может быть полностью числовым.</li></ul>"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Подтвердите пароль"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Введите тот же пароль, что и раньше, для проверки.</small></span>'

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    number = forms.CharField(
        label='Номер автомобиля',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Firmuser
        fields = ['first_name', 'last_name', 'email', 'phone', 'number', 'username', 'password']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'number': 'Номер автомобиля',
            'password': 'Пароль',
            
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            
    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        phone_number = self.cleaned_data['phone']
        if commit:
            user.save()
            Phone.objects.create(user=user, name=phone_number)
        return user