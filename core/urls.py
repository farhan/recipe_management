from django.conf.urls import url
from rest_framework import routers

from core import views

router = routers.DefaultRouter()

router.register(r'sign-up', views.SignUpViewSet, base_name='sign-up')
router.register(r'log-in', views.LoginViewSet, base_name='log-in')
router.register(r'profile-viewset', views.UserProfileViewSet)
router.register(r'following-viewset', views.UserFollowingViewSet)

urlpatterns = [
    url(r'^change-password-view/', views.ChangePasswordApiView.as_view()),
]

urlpatterns += router.urls
