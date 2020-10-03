from rest_framework import serializers

from user_profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'car_name', 'first_name', 'last_name', 'email', 'phone', 'imei', 'plat_number', 'avatar')
        read_only_fields = ('id',)
        lookup_field = 'id'

    def update(self, instance, validated_data):
        UserProfile.objects = validated_data
        instance.profile.save()
        return instance
