from django import forms
import datetime

from records.models import Category, Record

class CategoryForm(forms.ModelForm):
    color = forms.ChoiceField(
        label='Color',
        choices=[
            ('#E6B0AA', 'E6B0AA'),
            ('#D7BDE2', 'D7BDE2'),
            ('#A9CCE3', 'A9CCE3'),
            ('#A3E4D7', 'A3E4D7'),
            ('#A9DFBF', 'A9DFBF'),
            ('#F9E79F', 'F9E79F'),
            ('#F5CBA7', 'F5CBA7'),
            ('#ABB2B9', 'ABB2B9'),
            ('#CCD1D1', 'CCD1D1'),
            ('#E5E7E9', 'E5E7E9'),
        ],
        widget=forms.Select(attrs={'class':'form-control'})
    )
    class Meta:
        model = Category
        fields = ['name', 'color', 'description']
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


class RecordForm(forms.ModelForm):
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
    datetime = forms.DateTimeField(
        initial='',
        label='Date and Time',
        widget=forms.DateTimeInput(attrs={'class':'form-control', 'type': 'datetime-local'})
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
    
    class Meta:
        model = Record
        fields = ['title', 'is_income', 'category', 'value', 'datetime', 'description']

    def __init__(self, *args, **kwargs):

        if 'categories' not in kwargs:
            raise Category.DoesNotExist()

        categories = kwargs.pop('categories')
        print(categories)

        initial = kwargs.get('initial', {})
        
        now = datetime.datetime.now()
        initial['datetime'] = datetime.datetime(now.year, now.month, now.day, 12)
        
        print(kwargs.get('categories'))
        # initial['category'] = kwargs.get('categories')['name']
        
        kwargs['initial'] = initial        

        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = categories
