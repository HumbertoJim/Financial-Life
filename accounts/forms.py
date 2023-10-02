from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from accounts.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(
        initial='',
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'email'
        })
    )
    password = forms.CharField(
        initial='',
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'password'
        })
    )

class SignInForm(LoginForm):
    confirm_email = forms.EmailField(
        initial='',
        label='Confirm Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'confirm email'
        })
    )
    first_name = forms.CharField(
        initial='',
        label='First name',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'first name'
        }),
        required=False
    )
    last_name = forms.CharField(
        initial='',
        label='Last name',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'last name'
        }),
        required=False
    )
    password = forms.CharField(
        initial='',
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'password'
        })
    )
    confirm_password = forms.CharField(
        initial='',
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'confirm password'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('email already used')
        return email
    
    def clean_confirm_email(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        if email != confirm_email:
            raise ValidationError('email not matching')
        return confirm_email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password)
        return password
        
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')      
        if password != confirm_password:
            raise ValidationError('Passwords not matching')
        return confirm_password