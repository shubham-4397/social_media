"""
utility urls file
"""
# third party imports
from rest_framework import routers

# local imports
from apps.accounts.views import SignupViewSet, LoginViewSet


router = routers.SimpleRouter()

router.register('signup', SignupViewSet, 'signup')
router.register('login', LoginViewSet, 'login')

urlpatterns = [

] + router.urls
