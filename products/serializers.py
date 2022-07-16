from products.models import Product
from rest_framework import serializers
from authentication.models import UserProfile

class ProductSerializer(serializers.Serializer):
    user = serializers.CharField()
    name = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    tag_code = serializers.CharField()
    condition = serializers.CharField()
    specifications = serializers.CharField()
    link = serializers.CharField()
    price = serializers.CharField()

    def validate_user(self, value):
        user = UserProfile.objects.filter(uuid=value)
        if not user.exists():
            raise serializers.ValidationError("user does not exist")

        return value
    
    def create(self, validated_data):
        user = UserProfile.objects.get(uuid=validated_data['user'])
        validated_data['user'] = user
        product = Product.objects.create(**validated_data)
        return product