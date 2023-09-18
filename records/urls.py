from django.urls import path
from records.views import dashboard, RecordView, CategoryView

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('record', RecordView.as_view(), name='record'),
    path('category', CategoryView.as_view(), name='category'),
]