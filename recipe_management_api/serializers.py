from rest_framework import serializers

from core.serializers import UserProfileSerializer
from recipe_management_api import models


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = (
            'id',
            'title',
            'description',
            'stepwise_directions',
            'ingredients',
            'picture',
            'created_by'
        )
        extra_kwargs = {'created_by': {'read_only': True}}


class RecipeSerializerDetail(RecipeSerializer):
    created_by = UserProfileSerializer()
