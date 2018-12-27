from django.conf.urls import url
from django.conf.urls import include
from . import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r'recipe-viewset', views.RecipeViewSet, base_name='recipe-viewset')
router.register('followings-recipes-view', views.FollowingsRecipeViewSet, base_name='followings-recipes-view')

urlpatterns = [
    # path('farhan', views.RecipeViewSet),
]

urlpatterns += router.urls
