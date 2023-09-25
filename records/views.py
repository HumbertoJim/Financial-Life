from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from records.models import Record, Category
from records.forms import RecordForm, CategoryForm

from main.exceptions import NotAuthenticated

# Create your views here.
class RecordListView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            records = Record.objects.filter(user=request.user).select_related('category').order_by('-created_at')
            records = records.values('id', 'title', 'description', 'datetime', 'value', 'is_income', 'category__name', 'category__color')
            context = { 'records': records }
            return render(request, 'record_list.html', context)
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
            record = Record() if record_id == None else Record.objects.filter(user=request.user).get(id=record_id)
            form = RecordForm(instance=record, categories=categories)
            context = {
                'form': form,
                'categories': categories.values('name', 'color'),
                'record_id': record_id
            }
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
                raise Category.DoesNotExist()
            record = Record(user=request.user) if record_id == None else Record.objects.filter(user=request.user).get(id=record_id)
            form = RecordForm(request.POST, instance=record, categories=categories)
            if form.is_valid():
                record = form.save(commit=False)
                if record.category.user == request.user:
                    record.save()
                    messages.success(request, 'Record saved')
                else:
                    messages.error(request, 'Invalid category, record not saved')
                return redirect('/records/')
            context = {'form': form, 'categories': categories.values('name', 'color')}
            return render(request, 'record.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Record.DoesNotExist:
            messages.error(request, 'Error, invalid record')
            return redirect('/records/')
        except Category.DoesNotExist:
            messages.warning(request, 'You have not registered any category, please add one first.')
            return redirect('/records/categories/register')


class RecordDeleteView(View):
    def get(self, request, record_id):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            record = Record.objects.filter(user=request.user).get(id=record_id)
            context = {
                'record': {
                    'id': record.id,
                    'title': record.title,
                    'value': record.value,
                    'datetime': record.datetime,
                    'is_income': record.is_income,
                    'category__name': '' if record.category == None else record.category.name,
                    'category__color': '#ffffff' if record.category == None else record.category.color
                }
            }
            return render(request, 'record_delete.html', context)
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Record.DoesNotExist:
            messages.error(request, 'Error, invalid record')
            return redirect('/records/')
        
    def post(self, request, record_id=None):
        try:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
            record = Record.objects.filter(user=request.user).get(id=record_id)
            record.delete()
            messages.success(request, 'Record deleted')
            return redirect('/records/')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Record.DoesNotExist:
            messages.error(request, 'Error, invalid record')
            return redirect('/records/')


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
                return redirect('/records/categories/')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories/')
    
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
            return redirect('/records/categories/')
        except NotAuthenticated:
            return redirect('/accounts/login')
        except Category.DoesNotExist:
            messages.warning(request, 'Invalid category')
            return redirect('/records/categories/')
