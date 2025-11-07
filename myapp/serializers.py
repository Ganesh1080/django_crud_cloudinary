from rest_framework import serializers
from .models import new_crud
class CrudSerializer(serializers.ModelSerializer):
    class Meta:
        model=new_crud
        fields="__all__"