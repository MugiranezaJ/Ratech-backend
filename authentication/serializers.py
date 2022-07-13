# from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, UserProfile
from uuid import uuid4


# class UserLogoutSerializer(serializers.ModelSerializer):
    # token = serializers.CharField()
    # status = serializers.CharField(required=False, read_only=True)

    # def validate(self, data):
    #     token = data.get("token", None)
    #     print(token)
    #     user = None
    #     try:
    #         user = User.objects.get(token=token)
    #         if not user.ifLogged:
    #             raise ValidationError("User is not logged in.")
    #     except Exception as e:
    #         raise ValidationError(str(e))
    #     user.ifLogged = False
    #     user.token = ""
    #     user.save()
    #     data['status'] = "User is logged out."
    #     return data

    # class Meta:
    #     model = User
    #     fields = ('token','status')

class ReturnedUser:
    first_name = ""
    last_name = ""
    username = ""
    email = ""
    phone = ""
    role = ""
    gender = ""
    token = ""
    uuid = ""
    is_active = ""
    resident_city = ""
    resident_country = ""
    profile_image = ""

    def __init__(
            self,
            first_name,
            last_name,
            username,
            email,
            phone,
            role,
            gender,
            token,
            is_active,
            uuid,
            resident_city,
            resident_country,
            profile_image):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.phone = phone
        self.role = role
        self.gender = gender
        self.uuid = uuid
        self.token = token
        self.is_active = is_active
        self.resident_city = resident_city
        self.resident_country = resident_country
        self.profile_image = profile_image
class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    resident_city = serializers.CharField()
    resident_country = serializers.CharField()
    profile_image = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)
    role = serializers.CharField()
    gender = serializers.CharField()
    is_active = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        # Separate data for users model
        user_data = {
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        # Separate data for profile model
        profile_data = {
            "phone": self.context['phone'],
        }

        instance.phone = profile_data['phone']
        instance.save()

        user = instance.user
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']

        user.save()

        token = Token.objects.get(user=user)

        profile_data["uuid"] = instance.uuid
        returned_user = ReturnedUser(
            **user_data, **profile_data, token=token.key)

        return returned_user

        
    def create(self, validated_data):
        # Separate data for user model
        user_data = {
            "username": validated_data['email'],
            "email": validated_data['email'],
            "first_name": validated_data['first_name'],
            "last_name": validated_data['last_name'],
        }

        # Separate data for profile model
        profile_data = {
                "role": validated_data['role'],
                "is_active": False,
                "phone": validated_data.get('phone'),
                "gender": validated_data.get('gender'),
                "profile_image": validated_data.get('profile_image'),
                "resident_city": validated_data.get('resident_city'),
                "resident_country": validated_data.get('resident_country')
            }

        username = validated_data['username']
        if not self.user_exists(username):
            user = User.objects.create_user(
                **user_data
            )
            user.set_password(validated_data['password'])
            user.save()

             #  Create token for user
            token = Token.objects.create(
                user=user
            )
        else:
            user = User.objects.get(username=username)
            token = Token.objects.get(user=user)
       
        profile = UserProfile.objects.create(
            user=user,
            **profile_data
        )

        profile_data['uuid'] = profile.uuid

        returned_user = ReturnedUser(
            **user_data, **profile_data, token=token.key)

        return returned_user
    
    def user_exists(self, username):
        return User.objects.filter(username=username).exists()