from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, SignInForm
from main.exceptions import NotAuthenticated

from admin_panel.models import Setting
from accounts.models import User

# Create your views here.
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        context = {'form': LoginForm()}
        return render(request, 'login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid user or password')
        else:
            messages.error(request, 'Invalid fields')
        return render(request, 'login.html', {'form':form})
    
class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignInForm()
        context = {'form': form}
        return render(request, 'signin.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = SignInForm(request.POST)
        if form.is_valid():
            max_users = 0
            try:
                max_users = Setting.objects.get(name='max_users').value
                max_users = int(max_users)
            except:
                max_users = 0
            if User.objects.count() < max_users:
                new_user = User(
                    #username = form.cleaned_data.get('email'),
                    email = form.cleaned_data.get('email'),
                    first_name = form.cleaned_data.get('first_name', ''),
                    last_name = form.cleaned_data.get('last_name', '')
                )
                new_user.set_password(form.cleaned_data.get('password'))
                new_user.save()
                messages.success(request, 'User registered')
                return redirect('/accounts/login')
            messages.warning(request, 'Error, unable to sign-in in this moment. Please try later.')
        else:
            messages.error(request, 'Invalid fields')
        context = {'form': form}
        return render(request, 'signin.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

class ProfileView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            return render(request, 'profile.html')
        except NotAuthenticated:
            return redirect('/accounts/login')
        