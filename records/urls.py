from django.urls import path
from records.views import IncomeListView, IncomeView, IncomeDeleteView
from records.views import ExpenseListView, ExpenseView, ExpenseDeleteView
from records.views import CategoryListView, CategoryView, CategoryDeleteView

urlpatterns = [
    path('incomes', IncomeListView.as_view(), name='incomes'),
    path('incomes/register', IncomeView.as_view(), name='register_income'),
    path('incomes/<int:income_id>/edit', IncomeView.as_view(), name='edit_income'),
    path('incomes/<int:income_id>/delete', IncomeDeleteView.as_view(), name='delete_income'),
    
    path('expenses', ExpenseListView.as_view(), name='expenses'),
    path('expenses/register', ExpenseView.as_view(), name='register_expense'),
    path('expenses/<int:income_id>/edit', ExpenseView.as_view(), name='edit_expense'),
    path('expenses/<int:income_id>/delete', ExpenseDeleteView.as_view(), name='delete_expense'),

    path('categories', CategoryListView.as_view(), name='categories'),
    path('categories/register', CategoryView.as_view(), name='register_category'),
    path('categories/<int:category_id>/edit', CategoryView.as_view(), name='edit_category'),
    path('categories/<int:category_id>/delete', CategoryDeleteView.as_view(), name='delete_category'),
]