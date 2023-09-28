from django.shortcuts import render

from records.models import Record
import pandas as pd

def home(request):
    context = {'labels': [], 'values':[]}
    if request.user.is_authenticated:
        df = pd.DataFrame(list(Record.objects.filter(user=request.user).values('title', 'datetime', 'is_income', 'value', 'category__name', 'category__color')))
        df = df.rename(columns={
            'category__name': 'category',
            'category__color': 'color'
        })
        expenses = df[df['is_income']==False]
        expenses = expenses.groupby('category').sum('value').reset_index()
        print(expenses.head())
        context['labels'] =  expenses['category'].values
        context['values'] = expenses['value'].values
    return render(request, 'home.html', context)