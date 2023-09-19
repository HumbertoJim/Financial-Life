from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from records.models import Record, Category
from records.forms import RecordForm, CategoryForm
from records.serializers import RecordSerializer, CategorySerializer

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        categories = Category.objects.filter(user=request.user)
        category_serializer = CategorySerializer(categories, many=True)
        records = Record.objects.filter(user=request.user).order_by('-created_at')
        record_serializer = RecordSerializer(records, many=True)
        context = {
            'categories': category_serializer.data,
            'records': record_serializer.data,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/accounts/login')
    
class RecordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.filter(user=request.user)
            if categories.exists():
                category_serializer = CategorySerializer(categories, many=True)
                form = RecordForm()
                context = {
                    'form': form,
                    'categories': category_serializer.data
                }
                return render(request, 'record.html', context)
            else:
                return redirect('/records/category')
        else:
            return redirect('/accounts/login')
    
    def post(self, request):
        if request.user.is_authenticated:
            form = RecordForm(request.POST)
            if form.is_valid():
                data = {
                    'title': form.cleaned_data.get('title'),
                    'description': form.cleaned_data.get('description', ''),
                    'value': form.cleaned_data.get('value'),
                    'is_income': form.cleaned_data.get('is_income'),
                    'category': form.cleaned_data.get('category'),
                    'user': request.user.id
                }
                serializer = RecordSerializer(data=data)
                if serializer.is_valid():
                    messages.success(request, 'Record saved')
                    serializer.save()
                    return redirect('/records/dashboard')
                else:
                    print(serializer.errors)
                    print("SERIALIZER INVALID")
                    for field in serializer.errors:
                        for error in serializer.errors[field]:
                            messages.error(request, '{0}: {1}'.format(field.capitalize(), error.capitalize()))
            else:
                print("FORM INVALID")
                errors = form.errors.as_data()
                for field in errors:
                    for validation_error in errors[field]:
                        for error in validation_error:
                            messages.error(request, '{0}: {1}'.format(field.capitalize(), error.capitalize()))
            categories = Category.objects.filter(user=request.user)
            if categories.exists():
                category_serializer = CategorySerializer(categories, many=True)
                context = {
                    'form': form,
                    'categories': category_serializer.data
                }
                return render(request, 'record.html', context)
            else:
                return redirect('/records/category')
        else:
            return redirect('/accounts/login')
        
class CategoryView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = CategoryForm()
            context = {'form': form}
            return render(request, 'category.html', context)
        else:
            return redirect('/accounts/login')
    
    def post(self, request):
        if request.user.is_authenticated:
            form = CategoryForm(request.POST)
            if form.is_valid():
                data = {
                    'name': form.cleaned_data.get('name'),
                    'description': form.cleaned_data.get('description'),
                    'color': form.cleaned_data.get('color'),
                    'user': request.user.id
                }
                serializer = CategorySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    messages.success(request, 'Category saved')
                    return redirect('/records/dashboard')
                else:
                    for field in serializer.errors:
                        for error in serializer.errors[field]:
                            messages.error(request, '{0}: {1}'.format(field.capitalize(), error.capitalize()))
            else:
                errors = form.errors.as_data()
                for field in errors:
                    for validation_error in errors[field]:
                        for error in validation_error:
                            messages.error(request, '{0}: {1}'.format(field.capitalize(), error.capitalize()))
            return render(request, 'category.html', {'form': form})
        else:
            return redirect('/accounts/login')