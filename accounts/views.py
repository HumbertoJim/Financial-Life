from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm

# Create your views here.
class Login(View):
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid user or password')
        else:
            messages.error(request, form.errors)
        return render(request, 'login.html', {'form':form})
    

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')