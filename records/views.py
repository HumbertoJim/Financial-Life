from django.shortcuts import render, redirect
from django.views import View

from records.models import Record, Category
from records.serializers import RecordSerializer, CategorySerializer

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        records = Record.objects.filter(user=request.user).order_by('-created_at')
        serializer = RecordSerializer(records, many=True)
        context = {
            'records': serializer.data
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/accounts/login')
    
class RecordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.filter(user=request.user)
            if categories.exists():
                serializer = CategorySerializer(categories, many=True)
                context = {
                    'categories': serializer.data
                }
                return render(request, 'record.html', context)
            else:
                return redirect('/records/category')
        else:
            return redirect('/accounts/login')
    
    def post(self, request):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('/accounts/login')
        
class CategoryView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'category.html')
        else:
            return redirect('/accounts/login')
    
    def post(self, request):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('/accounts/login')