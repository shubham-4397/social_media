from django.db.models import Q, OuterRef, Subquery
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

# local imports
from apps.social.filters import NameEmailFilters
from apps.social.messages import SUCCESS_MESSAGE, ERROR_MESSAGE
from apps.social.models import FriendRequest
from apps.social.pagination import return_paginated_response
from apps.social.serializers import (OtherUsersSerializer, FriendRequestSerializer, PendingRequestSerializer,
                                     MyFriendsSerializer)

USER = get_user_model()


class OtherUsersViewSet(GenericViewSet, mixins.ListModelMixin):
    """used to list other users"""
    serializer_class = OtherUsersSerializer
    queryset = USER.objects.all().exclude(Q(is_staff=True) | Q(is_active=False))
    permission_classes = [IsAuthenticated]
    filterset_class = NameEmailFilters

    def list(self, request, *args, **kwargs):
        """used to list the other users who are not in friends list"""
        all_users = self.get_queryset().exclude(id=self.request.user.id)
        accepted_friends = FriendRequest.objects.filter(
            Q(from_user=OuterRef('pk'), to_user=self.request.user) |
            Q(from_user=self.request.user, to_user=OuterRef('pk')), is_accepted=True).values('id')

        qs = all_users.exclude(Q(id__in=Subquery(accepted_friends.values('from_user'))) |
                               Q(id__in=Subquery(accepted_friends.values('to_user'))))
        filtered_query = self.filter_queryset(queryset=qs)
        return return_paginated_response(self.serializer_class, request, filtered_query)


class FriendRequestViewSet(GenericViewSet):
    """used to send/receive friend requests"""
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return FriendRequestSerializer

    @action(methods=['post'], url_name="send", url_path="send", detail=False, serializer_class=FriendRequestSerializer)
    def send_request(self, request, *args, **kwargs):
        """used to send the friend request"""
        serializer = self.get_serializer_class()(data=request.data, context={'from_user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": SUCCESS_MESSAGE['request-sent']})

    @action(methods=['patch'], url_name="accept", url_path="accept", detail=True, serializer_class=None)
    def accept_request(self, request, *args, **kwargs):
        """used to accept the friend request"""
        qs = self.get_queryset().filter(pk=kwargs.get("pk"), to_user=request.user, is_accepted=False).first()
        if not qs:
            return Response({"details": ERROR_MESSAGE["request-not-found"]}, status=status.HTTP_404_NOT_FOUND)
        qs.is_accepted = True
        qs.save(update_fields=["is_accepted"])
        return Response({"details": SUCCESS_MESSAGE["request-accepted"]})

    @action(methods=['delete'], url_name="reject", url_path="reject", detail=True, serializer_class=None)
    def reject_request(self, request, *args, **kwargs):
        """used to reject the friend request"""
        qs = self.get_queryset().filter(pk=kwargs.get("pk"), to_user=request.user).first()
        if not qs:
            return Response({"details": ERROR_MESSAGE["request-not-found"]}, status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response({"details": SUCCESS_MESSAGE["request-rejected"]})

    @action(methods=['get'], url_name="pending", url_path="pending", detail=False,
            serializer_class=PendingRequestSerializer)
    def pending_request(self, request, *args, **kwargs):
        """used to get the pending requests of the current user"""
        qs = self.get_queryset().filter(to_user=request.user, is_accepted=False).select_related("from_user")
        return return_paginated_response(self.serializer_class, request, qs)

    @action(methods=['get'], url_name="my-friends", url_path="my-friends", detail=False,
            serializer_class=MyFriendsSerializer)
    def my_friends(self, request, *args, **kwargs):
        """used to get the friends of the current user"""
        qs = self.get_queryset().filter(Q(from_user=request.user, is_accepted=True) |
                                        Q(to_user=request.user, is_accepted=True)).select_related("from_user",
                                                                                                  "to_user")
        return return_paginated_response(self.serializer_class, request, qs)
