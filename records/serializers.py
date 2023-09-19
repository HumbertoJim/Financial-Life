from rest_framework import serializers

from records.models import Record, Category


class CategorySerializer(serializers.ModelSerializer):
    def validate_value(self, value):
        if len(value) != 7:
            raise serializers.ValidationError({'name': 'invalid color'})
        if value[0] != '#':
            raise serializers.ValidationError({'name': 'invalid color'})
        for c in value[1:]:
            if c.lower() not in '0123456789abcdef':
                raise serializers.ValidationError({'name': 'invalid color'})
        return value
    
    def validate(self, data):
        if Category.objects.filter(user=data['user']).filter(name=data['name']).exists():
            raise serializers.ValidationError({'name': 'a category with the same name exists'})
        return super().validate(data)
    
    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'color': instance.color,
        }
        return representation
    
    class Meta:
        model = Category
        fields =['id', 'name', 'description', 'color', 'user']

class RecordSerializer(serializers.ModelSerializer):
    is_income = serializers.IntegerField()
    def validate_is_income(self, value):
        if value <= 0:
            return False
        return True

    def validate(self, data):
        if data['user'] != data['category'].user:
            raise serializers.ValidationError({'category': 'invalid category'})
        return super().validate(data)
    
    def to_representation(self, instance):
        representation = {
            'title': instance.title,
            'description': instance.description,
            'value': instance.value,
            'is_income': instance.is_income,
            'category': 'Other' if instance.category != None else instance.category.name
        }
        return representation
    
    class Meta:
        model = Record
        fields =['title', 'description', 'value', 'is_income', 'category', 'user']
        extra_kwargs = {
            'description': {'allow_blank':True}
        }
