from rest_framework import serializers
from .models import Item, Outfit, UserPreference

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'aesthetic', 'category', 'image_url']

class OutfitSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Outfit
        fields = ['id', 'items', 'aesthetic']

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['id', 'user', 'preferred_aesthetics']