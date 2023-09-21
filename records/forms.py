from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList

from records.models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(initial='', required=True)
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']

class RecordForm(forms.Form):
    title = forms.CharField(
        initial='',
        label='Title',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    is_income = forms.ChoiceField(
        initial=0,
        choices=[(0, 'Expense'), (1, 'Income')],
        label='Type',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        to_field_name='name',
        label='Category',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    value = forms.FloatField(
        initial=0,
        min_value=0,
        label='Ammount ($)',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        initial='',
        label='Description',
        widget=forms.Textarea(attrs={'class':'form-control', 'rows': '3'}),
        required=False,
    )

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = categories