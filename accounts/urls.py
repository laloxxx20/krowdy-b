from rest_framework import routers

from . import views

app_name = 'accounts'

router = routers.SimpleRouter()
router.register(
    r'user', views.UserView, base_name='user')
router.register(
    r'user-emails', views.EmailView, base_name='user-emails')
router.register(
    r'user-phones', views.PhoneView, base_name='user-phones')

urlpatterns = router.urls
