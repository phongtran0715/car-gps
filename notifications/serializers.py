from rest_framework import serializers

from notifications.models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('body', 'title', 'image', 'url', 'created_at')
