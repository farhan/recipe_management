from rest_framework import serializers

from core import models


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'password', 'mobile_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            mobile_number=validated_data['mobile_number'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.save()
        return instance


class UserFollowingSerializer(serializers.ModelSerializer):
    """A serializer for our UserFollowing objects."""

    class Meta:
        model = models.UserFollowing
        fields = ('id', 'following', 'created_on',)


class UserFollowingSerializerDetail(UserFollowingSerializer):
    """A serializer for our UserFollowing objects."""
    following = UserProfileSerializer()


class UserFollowerSerializer(serializers.ModelSerializer):
    """A serializer for UserFollowing Followers objects."""

    user = UserProfileSerializer()

    class Meta:
        model = models.UserFollowing
        fields = ('id', 'user')
