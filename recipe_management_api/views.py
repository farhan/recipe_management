# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import UserFollowing
from core.serializers import UserFollowingSerializerDetail
from recipe_management_api import serializers, models
from recipe_management_api.permissions import CreateOwnRecipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ View set for recipe model """

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    permission_classes = (CreateOwnRecipe, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the recipe owner to the logged in user."""

        serializer.save(created_by=self.request.user)


class FollowingsRecipeViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """Return the recipes of followings (others followed by user)."""

        followings = UserFollowing.objects.filter(user__id=request.user.id)
        following_user_ids = []
        for following in followings:
            following_user_ids.append(following.following.id)
        followings_recipes = models.Recipe.objects.filter(created_by__id__in=following_user_ids)

        followings_serializer = UserFollowingSerializerDetail(followings, many=True)
        followings_recipes_serializer = serializers.RecipeSerializerDetail(followings_recipes, many=True)

        return Response(
            {
                'message': 'List of recipes of users followed by ' + request.user.username,
                'followings_list': followings_serializer.data,
                'followings recipes list': followings_recipes_serializer.data
            }
        )
