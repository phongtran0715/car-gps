from rest_framework import serializers

from user_profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('car_name', 'first_name', 'last_name', 'email', 'phone', 'imei', 'plate_number', 'avatar', 'is_active')
