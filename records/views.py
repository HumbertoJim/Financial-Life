from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from records.models import Income, Expense, Category
from records.forms import RecordForm, CategoryForm

from main.exceptions import NotAuthenticated

# Create your views here.
class IncomeListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            incomes = Income.objects.filter(user=request.user).order_by('-date')
            incomes = incomes.values('id', 'title', 'description', 'date', 'value', 'category__name', 'category__color')
            context = { 'incomes': incomes }
            return render(request, 'income_list.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')

class IncomeView(View):
    def get(self, request, income_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                raise Category.DoesNotExist()
            income = Income() if income_id == None else Income.objects.filter(user=request.user).get(id=income_id)
            form = RecordForm(instance=income, categories=categories)
            context = {
                'form': form,
                'categories': categories.values('name', 'color'),
                'income_id': income_id
            }
            return render(request, 'income.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Income.DoesNotExist:
            messages.error(request, 'Error, invalid income')
            return redirect('/records/incomes')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categories/register')
        
    def post(self, request, income_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                raise Category.DoesNotExist()
            income = Income(user=request.user) if income_id == None else Income.objects.filter(user=request.user).get(id=income_id)
            form = RecordForm(request.POST, instance=income, categories=categories)
            if form.is_valid():
                income = form.save(commit=False)
                if income.category.user == request.user:
                    income.save()
                    messages.success(request, 'Income saved')
                else:
                    messages.error(request, 'Invalid category, income was not saved')
                return redirect('/records/incomes')
            else:
                messages.error(request, 'Invalid fields')
            context = {'form': form, 'categories': categories.values('name', 'color')}
            return render(request, 'income.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Income.DoesNotExist:
            messages.error(request, 'Error, invalid income')
            return redirect('/records/incomes')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categoriesregister')

class IncomeDeleteView(View):
    def get(self, request, income_id):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            income = Income.objects.filter(user=request.user).get(id=income_id)
            context = {
                'income': {
                    'id': income.id,
                    'title': income.title,
                    'value': income.value,
                    'date': income.date,
                    'category__name': '' if income.category == None else income.category.name,
                    'category__color': '#ffffff' if income.category == None else income.category.color
                }
            }
            return render(request, 'income_delete.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Income.DoesNotExist:
            messages.error(request, 'Error, invalid income')
            return redirect('/records/incomes')
        
    def post(self, request, income_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            income = Income.objects.filter(user=request.user).get(id=income_id)
            income.delete()
            messages.success(request, 'Income deleted')
            return redirect('/records/incomes')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Income.DoesNotExist:
            messages.error(request, 'Error, invalid income')
            return redirect('/records/incomes')

class ExpenseListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            expenses = Expense.objects.filter(user=request.user).order_by('-date')
            expenses = expenses.values('id', 'title', 'description', 'date', 'value', 'category__name', 'category__color')
            context = { 'expenses': expenses }
            return render(request, 'expense_list.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')

class ExpenseView(View):
    def get(self, request, expense_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                raise Category.DoesNotExist()
            expense = Expense() if expense_id == None else Expense.objects.filter(user=request.user).get(id=expense_id)
            form = RecordForm(instance=expense, categories=categories)
            context = {
                'form': form,
                'categories': categories.values('name', 'color'),
                'expense_id': expense_id
            }
            return render(request, 'expense.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Expense.DoesNotExist:
            messages.error(request, 'Error, invalid expense')
            return redirect('/records/expenses')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categories/register')
        
    def post(self, request, expense_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                raise Category.DoesNotExist()
            expense = Expense(user=request.user) if expense_id == None else Expense.objects.filter(user=request.user).get(id=expense_id)
            form = RecordForm(request.POST, instance=expense, categories=categories)
            if form.is_valid():
                expense = form.save(commit=False)
                if expense.category.user == request.user:
                    expense.save()
                    messages.success(request, 'Expense saved')
                else:
                    messages.error(request, 'Invalid category, expense was not saved')
                return redirect('/records/expenses')
            else:
                messages.error(request, 'Invalid fields')
            context = {'form': form, 'categories': categories.values('name', 'color')}
            return render(request, 'expense.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Expense.DoesNotExist:
            messages.error(request, 'Error, invalid expense')
            return redirect('/records/expenses')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/expenses/categories/register')

class ExpenseDeleteView(View):
    def get(self, request, expense_id):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            expense = Expense.objects.filter(user=request.user).get(id=expense_id)
            context = {
                'expense': {
                    'id': expense.id,
                    'title': expense.title,
                    'value': expense.value,
                    'date': expense.date,
                    'category__name': '' if expense.category == None else expense.category.name,
                    'category__color': '#ffffff' if expense.category == None else expense.category.color
                }
            }
            return render(request, 'expense_delete.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Expense.DoesNotExist:
            messages.error(request, 'Error, invalid expense')
            return redirect('/records/expenses')
        
    def post(self, request, expense_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            expense = Expense.objects.filter(user=request.user).get(id=expense_id)
            expense.delete()
            messages.success(request, 'Expense deleted')
            return redirect('/records/expenses')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Expense.DoesNotExist:
            messages.error(request, 'Error, invalid expense')
            return redirect('/records/expenses')


class CategoryListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            categories = categories.values('id', 'name', 'description', 'color')
            context = {'categories': categories}
            return render(request, 'category_list.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')


class CategoryView(View):
    def get(self, request, category_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            category = Category() if category_id == None else Category.objects.filter(user=request.user).get(id=category_id)
            form = CategoryForm(instance=category)
            context = {'form': form, 'category_id': category.id}
            return render(request, 'category.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories')
    
    def post(self, request, category_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            category = Category(user=request.user) if category_id == None else Category.objects.filter(user=request.user).get(id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                user_categories = Category.objects.filter(user=request.user)
                if category_id:
                    user_categories = user_categories.exclude(id=category_id)
                if user_categories.filter(name=form.cleaned_data['name']).exists():
                    form.add_error('name', 'Name in use')
                else:
                    form.save()
                    messages.success(request, 'Category saved')
                    return redirect('/records/categories')
            else:
                messages.error(request, 'Invalid fields')
            context = {'form': form}
            return render(request, 'category.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories')
    
class CategoryDeleteView(View):
    def get(self, request, category_id):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if categories.count() > 1:
                category = categories.get(id=category_id)
                context = {
                    'category': {
                        'id': category.id,
                        'name': category.name,
                        'description': category.description,
                        'color': category.color
                    }
                }
                return render(request, 'category_delete.html', context)
            else:
                messages.error(request, 'Unable to delete the category because you must have at least one')
                return redirect('/records/categories')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories')
    
    def post(self, request, category_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if categories.count() > 1:
                category = categories.get(id=category_id)
                category.delete()
                messages.success(request, 'Category deleted')
            else:
                messages.error(request, 'Unable to delete the category because you must have at least one')
            return redirect('/records/categories')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories')
