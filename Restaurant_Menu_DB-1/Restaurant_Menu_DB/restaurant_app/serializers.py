from rest_framework import serializers
from .models import MenuSection

class MenuSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSection
        fields = ['id', 'name', 'display_order', 'menu']
