from django.urls import path
from records.views import RecordListView, RecordView, RecordDeleteView
from records.views import CategoryListView, CategoryView, CategoryDeleteView

urlpatterns = [
    path('', RecordListView.as_view(), name='records'),
    path('register', RecordView.as_view(), name='register_record'),
    path('<int:record_id>/edit', RecordView.as_view(), name='edit_record'),
    path('<int:record_id>/delete', RecordDeleteView.as_view(), name='delete_record'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/register', CategoryView.as_view(), name='register_category'),
    path('categories/<int:category_id>/edit', CategoryView.as_view(), name='edit_category'),
    path('categories/<int:category_id>/delete', CategoryDeleteView.as_view(), name='delete_category'),
]