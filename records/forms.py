from django import forms
from records.models import Category, Income, Expense
import datetime

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


class RecordForm(forms.Form):
    title = forms.CharField(
        initial='',
        label='Title',
        widget=forms.TextInput(attrs={'class':'form-control'})
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
    date = forms.DateField(
        initial='',
        label='Date',
        widget=forms.DateInput(attrs={'class':'form-control', 'type': 'date'})
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
    
    def save(self, commit=True):
        if self.instance:
            self.instance.title = self.cleaned_data.get('title')
            self.instance.category = self.cleaned_data.get('category')
            self.instance.date = self.cleaned_data.get('date')
            self.instance.value = self.cleaned_data.get('value')
            self.instance.description = self.cleaned_data.get('description')
            if commit:
                self.instance.save()
            return self.instance
        raise Exception('Unable to save form with non instance fixed')
    
    def __init__(self, *args, **kwargs):

        if 'instance' not in kwargs:
            raise Exception('Unable to init form with non instance fixed')

        if 'categories' not in kwargs:
            raise Category.DoesNotExist()
        
        self.instance = kwargs.pop('instance')

        if not (isinstance(self.instance, Income) or isinstance(self.instance, Expense)):
            raise Exception('Instance must be an instance from Income or Expense model')

        categories = kwargs.pop('categories')

        initial = kwargs.get('initial', {})
        
        today = datetime.date.today()
        initial['date'] = datetime.date(today.year, today.month, today.day)
        
        kwargs['initial'] = initial        

        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = categories
