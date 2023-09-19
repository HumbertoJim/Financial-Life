from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput)