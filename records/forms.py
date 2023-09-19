from django import forms

from records.models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(initial='', required=True)
    class Meta:
        model = Category
        fields = ['name', 'description', 'color']

class RecordForm(forms.Form):
    title = forms.CharField(initial='', required=True)
    description = forms.CharField(initial='', required=False)
    value = forms.FloatField(initial=0, min_value=0, required=True)
    is_income = forms.IntegerField(initial=0, required=True)
    category = forms.IntegerField()