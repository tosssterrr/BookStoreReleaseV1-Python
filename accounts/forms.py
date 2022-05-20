from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, AuthenticationForm, PasswordChangeForm, \
    UserCreationForm
from django import forms

User = get_user_model()


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Форма для изменения пароля авторизированного пользователя
    """
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'autofocus': True,
                                          'class': 'form-control w-25'
                                          }),
    )
    new_password1 = forms.CharField(max_length=20,
                                    help_text=password_validation.password_validators_help_text_html(),
                                    label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))
    new_password2 = forms.CharField(max_length=20,
                                    label='Повторение пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))


class UserPasswordResetForm(PasswordResetForm):
    """
    Форма для отправки почты для сброса пароля
    """
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control w-25',
        'placeholder': 'Email',
    }))


class UserSetPasswordForm(SetPasswordForm):
    """
    Форма для ввода пароля по ссылке-токену
    """
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(max_length=20,
                                    help_text=password_validation.password_validators_help_text_html(),
                                    label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))
    new_password2 = forms.CharField(max_length=20,
                                    label='Повторение пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))


class UserLoginForm(AuthenticationForm):
    '''
    Базовая логин-форма
    '''
    username = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    password = forms.CharField(max_length=22, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=22, label='Имя пользователя', min_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=22, label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=22, label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')