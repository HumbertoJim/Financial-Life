from django.shortcuts import render, redirect

from records.models import Expense, Income
import pandas as pd

def home(request):
    if request.user.is_authenticated:
        try:
            try:
                incomes = list(Income.objects.filter(user=request.user).values('date', 'value', 'category__name'))
            except:
                incomes = []
            incomes = {'date':[], 'value':[], 'category__name': []} if incomes == [] else incomes
            df_incomes = pd.DataFrame(incomes)
            df_incomes['value'] = [abs(i) for i in df_incomes['value']]

            try:
                expenses = list(Expense.objects.filter(user=request.user).values('date', 'value', 'category__name'))
            except:
                expenses = []
            expenses = {'date':[], 'value':[], 'category__name': []} if expenses == [] else expenses
            df_expenses = pd.DataFrame(expenses)
            df_expenses['positive_value'] = [abs(i) for i in df_expenses['value']]
            df_expenses['value'] = -df_expenses['positive_value']

            df = pd.concat([df_incomes, df_expenses])
            df_records = df.groupby('date').sum('value').reset_index().sort_values('date')
            df_incomes = df_incomes.groupby('category__name').sum('value').reset_index()
            df_expenses = df_expenses.groupby('category__name').sum('positive_value').reset_index()

            context = {
                'labels': df_records['date'].values,
                'values': df_records['value'].values,
                'labels_expenses': df_expenses['category__name'].values,
                'values_expenses': df_expenses['positive_value'].values,
                'labels_incomes': df_incomes['category__name'].values,
                'values_incomes': df_incomes['value'].values,
            }
        except:
            context = {
                'labels': [],
                'values': [],
                'labels_expenses': [],
                'values_expenses': [],
                'labels_incomes': [],
                'values_incomes': [],
            }
        return render(request, 'home.html', context)
    else:
        return redirect('/accounts/login')