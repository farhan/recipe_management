from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from core import models, serializers, permissions
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication

from core.serializers import ChangePasswordSerializer
from recipe_management import settings


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, creating and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    http_method_names = ['get', 'post', 'head', 'patch']

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class SignUpViewSet(viewsets.ViewSet):
    """User Sign Up ViewSet."""

    serializer_class = serializers.UserProfileSerializer

    def create(self, request):
        """Create a and return a new object of UserProfile."""

        serializer = serializers.UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            username = serializer.data.get('username')
            message = "Account for '{0}' created successfully".format(username)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApiView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = settings.AUTH_USER_MODEL
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def patch(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not check_password(serializer.data.get("old_password"), request.user.password):
                return Response({"error_message": "Old password is wrong."}, status=status.HTTP_400_BAD_REQUEST)
            # Check password changed
            if check_password(serializer.data.get("new_password"), request.user.password):
                return Response({"error_message": "Old password and new password are same."},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            return Response("Password updated successfully.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowingViewSet(viewsets.ModelViewSet):
    """Handles creating, creating and updating profiles."""

    serializer_class = serializers.UserFollowingSerializer
    queryset = models.UserFollowing.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user=self.request.user)

    def list(self, request):
        """Return a list of followers."""

        followers = models.UserFollowing.objects.filter(following__id=request.user.id)

        serializer = serializers.UserFollowerSerializer(followers, many=True)

        return Response({
            'message': 'Followers of ' + request.user.username,
            'followers_list': serializer.data
        })
