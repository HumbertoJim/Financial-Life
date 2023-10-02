from django.urls import path
from accounts.views import LoginView, SignInView, logout, ProfileView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signin', SignInView.as_view(), name='sign_in'),
    path('logout', logout, name='logout'),
    path('profile', ProfileView.as_view(), name='profile')
]