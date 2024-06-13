from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.social.messages import ERROR_MESSAGE
# local imports
from apps.social.models import FriendRequest


USER = get_user_model()


class OtherUsersSerializer(serializers.ModelSerializer):
    """
    Used to find the other users
    """
    class Meta:
        model = USER
        fields = ['id', 'email', 'first_name', 'last_name']


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    used to send the request
    """
    to_user = serializers.IntegerField()

    class Meta:
        model = FriendRequest
        fields = ("to_user", )

    def validate(self, attrs):
        """validate the database entries"""
        to_user = attrs.get('to_user')
        from_user = self.context.get("from_user")
        if to_user == from_user.id:
            raise serializers.ValidationError(ERROR_MESSAGE['self-request'])
        qs = USER.objects.filter(id=to_user).first()
        if not qs:
            raise serializers.ValidationError(ERROR_MESSAGE['user-not-found'])
        qs1 = FriendRequest.objects.all()
        if qs1.filter(to_user=qs, from_user=from_user).exists():
            raise serializers.ValidationError(ERROR_MESSAGE["request-already-exist"])
        one_minute = timezone.now() - timedelta(minutes=1)
        qs2 = qs1.filter(from_user=from_user, timestamp__gte=one_minute).count()
        if qs2 >= 3:
            raise serializers.ValidationError(ERROR_MESSAGE["request-exceed"])
        self.context.update({"to_user": qs})
        return attrs

    def create(self, validated_data):
        """
        create the request
        """
        qs = FriendRequest(to_user=self.context.get("to_user"), from_user=self.context.get("from_user"))
        qs.save()
        return qs


class PendingRequestSerializer(serializers.ModelSerializer):
    """
    used to list the pending requests
    """
    from_user = OtherUsersSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user"]


class MyFriendsSerializer(serializers.ModelSerializer):
    """used to serialize the objects"""

    class Meta:
        model = FriendRequest
        fields = ['email', 'first_name', 'last_name']

    def get_friend(self, obj):
        request_user = self.context['request'].user
        return obj.to_user if obj.from_user == request_user else obj.from_user

    def to_representation(self, instance):
        obj = self.get_friend(instance)
        return {
            'email': obj.email,
            'first_name': obj.first_name,
            'last_name': obj.last_name
        }
