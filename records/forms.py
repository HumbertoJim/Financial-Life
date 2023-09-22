from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from records.models import Category

class CategoryForm(forms.ModelForm):
    color = forms.ChoiceField(
        initial='#5499C7',
        label='Color',
        choices=[
            ('#5499C7', '#5499C7'),
            ('#48C9B0', '#48C9B0'),
            ('#58D68D', '#58D68D'),
            ('#F4D03F', '#F4D03F'),
            ('#DC7633', '#DC7633'),
            ('#EC7063', '#EC7063'),
            ('#F0F3F4', '#F0F3F4'),
            ('#AAB7B8', '#AAB7B8'),
            ('#5D6D7E', '#5D6D7E')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']
        labels = {
            'name': 'Name',
            'description': 'Description'
        }
        initial = {
            'name': '',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows':'3'})
        }


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
        empty_label=None,
        label='Category',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    value = forms.FloatField(
        initial=0,
        min_value=0,
        label='Amount ($)',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        initial='',
        label='Description',
        widget=forms.Textarea(attrs={'class':'form-control', 'rows': '3'}),
        required=False,
    )

    def clean_value(self):
        value = self.cleaned_data['value']
        if value < 0:
            raise forms.ValidationError({'value': 'Amount can not be negative'})
        return value

    def __init__(self, categories, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['category'] = categories.first().name
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = categories
