from email.policy import default
from products.models import Order, Product
from rest_framework import serializers
from authentication.models import UserProfile

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    name = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    tag_code = serializers.CharField()
    condition = serializers.CharField()
    specifications = serializers.CharField()
    link = serializers.CharField()
    price = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'

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
    
# class UserProfileSerializerWithDetails(serializers.ModelSerializer):
#     user = UserRegisterSerializer(read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = '__all__'
# class OrderSelializerWithProducts(serializers.ModelSerializer):
#     class Meta:
#         m
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    product = serializers.CharField()
    type = serializers.CharField()
    status = serializers.CharField(default='Processing')
    products= serializers.SerializerMethodField()

    class Meta:
            model = Order
            fields = "__all__"

    def get_products(self, obj):
        # print(obj.product)
        product = ProductSerializer(obj.product)
        return product.data

    def validate_user(self, value):
        user = UserProfile.objects.filter(uuid=value)
        if not user.exists():
            raise serializers.ValidationError("user does not exist")
        return value
    def validate_product(self, value):
        product = Product.objects.filter(uuid=value)
        if not product.exists():
            raise serializers.ValidationError("product deos not exist")
        return value

    def create(self, validated_data):
        user = UserProfile.objects.get(uuid=validated_data['user'])
        product = Product.objects.get(uuid=validated_data['product'])
        # order = Order.objects.filter(user=user, product=product, type=validated_data['type'])

        # if order.exists():
        #     return order.first()

        validated_data['product'] = product
        validated_data['user'] = user
        query = Order.objects.create(**validated_data)
        print(type(query))
        return query