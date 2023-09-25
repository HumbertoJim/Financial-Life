from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from records.models import Record, Category
from records.forms import RecordForm, CategoryForm

from main.exceptions import NotAuthenticated, DuplicatedValue

# Create your views here.
class RecordListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            records = Record.objects.filter(user=request.user).select_related('category').order_by('-created_at')
            records = records.values('id', 'title', 'description', 'datetime', 'value', 'is_income', 'category__name', 'category__color')
            context = { 'records': records }
            return render(request, 'records.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
    
class RecordView(View):
    def get(self, request, record_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                raise Category.DoesNotExist()
            categories = categories.values('name', 'color')
            record = Record() if record_id == None else Record.objects.filter(user=request.user).get(id=record_id)
            form = RecordForm(instance=record, categories=categories)
            context = {'form': form, 'categories': categories}
            return render(request, 'record.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Record.DoesNotExist:
            messages.error(request, 'Error, invalid record')
            return redirect('/records/')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categories/register')
        
    def post(self, request, record_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            if not categories.exists():
                print("F")
                raise Category.DoesNotExist()
            print("NoF")
            categories = categories.values('name', 'color')
            record = Record(user=request.user) if record_id == None else Record.objects.filter(user=request.user).get(id=record_id)
            form = RecordForm(request.POST, instance=record, categories=categories)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record saved')
                return redirect('/records/')
            context = {'form': form, 'categories': categories}
            return render(request, 'records.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Record.DoesNotExist:
            messages.error(request, 'Error, invalid record')
            return redirect('/records/')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categories/register')
        
class CategoryListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            categories = Category.objects.filter(user=request.user)
            categories = categories.values('id', 'name', 'description', 'color')
            context = {'categories': categories}
            return render(request, 'categories.html', context)
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
            return redirect('/records/categories/')
    
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
                    return redirect('/records/categories/')
            context = {'form': form}
            return render(request, 'category.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories/')
    
