from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class FriendRequest(models.Model):
    """
    request model to send accept and reject the requests
    """
    from_user = models.ForeignKey(USER, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(USER, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        """Meta class"""
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        """str representation"""
        return str(self.to_user)
