from django.urls import path
from records.views import RecordListView, RecordView, CategoryListView, CategoryView

urlpatterns = [
    path('', RecordListView.as_view(), name='records'),
    path('register', RecordView.as_view(), name='register_record'),
    path('<int:category_id>/edit', RecordView.as_view(), name='edit_record'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/register', CategoryView.as_view(), name='register_category'),
    path('categories/<int:category_id>/edit', CategoryView.as_view(), name='edit_category'),
]