"""
utility urls file
"""
# third party imports
from rest_framework import routers

# local imports
from apps.social.views import OtherUsersViewSet, FriendRequestViewSet


router = routers.SimpleRouter()

router.register('other-users', OtherUsersViewSet, 'other-users')
router.register('request', FriendRequestViewSet, 'request')

urlpatterns = [

] + router.urls
