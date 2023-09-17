from django.urls import path
from accounts.views import Login, logout

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout')
]