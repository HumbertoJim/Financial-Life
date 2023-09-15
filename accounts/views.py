from django.shortcuts import render
from django.views import View

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

# Create your views here.
class Login(View):
    def get(self, request):
        context = {'form': AuthenticationForm()}
        return render(request, 'login.html', context)
    
    def post(self, request):
        form = AuthenticationForm(request.POST)
        return render(request, 'login.html', {'form':form})
    