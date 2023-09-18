from rest_framework import serializers

from records.models import Record, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'name', 'color', 'description']

class RecordSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = {
            'name': instance.name,
            'description': instance.description,
            'value': instance.value,
            'is_income': instance.is_income,
            'category': 'Other' if instance.category != None else instance.category.name
        }
        return representation
    
    class Meta:
        model = Record
        fields =['name', 'description', 'value', 'is_income', 'category']
