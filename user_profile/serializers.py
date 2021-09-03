from rest_framework import serializers
import uuid
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User, UserRelationship

class UserSerializer(serializers.ModelSerializer):
    id              = serializers.UUIDField(default=uuid.uuid4,read_only=True)
    phone_number    = PhoneNumberField()
    display_name    = serializers.CharField(max_length=50,required=False)
    username        = serializers.CharField(max_length=50, required=False)
    display_image   = serializers.ImageField(required=False)
    isVerified      = serializers.BooleanField(default=False)
    otp             = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id','phone_number','display_name','username','display_image','isVerified','otp']

class UserVerifySerializer(serializers.Serializer):
    phone_number    = PhoneNumberField()
    otp             = serializers.IntegerField()


