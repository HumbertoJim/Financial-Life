from django.urls import path
from accounts.views import Login, logout, Profile

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('profile', Profile.as_view(), name='profile')
]