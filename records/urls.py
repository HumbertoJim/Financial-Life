from django.urls import path
from records.views import RecordView, CreateRecordView, CategoryView, CreateCategoryView

urlpatterns = [
    path('', RecordView.as_view(), name='records'),
    path('register', CreateRecordView.as_view(), name='register_record'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/register', CreateCategoryView.as_view(), name='register_category'),
]