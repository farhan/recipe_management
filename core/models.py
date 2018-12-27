from django.contrib.auth.models import AbstractUser
from django.db import models
from core import validators


class UserProfile(AbstractUser):
    mobile_number = models.CharField(
        max_length=12,
        validators=[validators.PhoneNumberValidator()],
    )

    def __str__(self):
        return self.email


class UserFollowing(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, related_name='user', on_delete=models.CASCADE)
    # Above user is following the below user
    following = models.ForeignKey(UserProfile, related_name='user_following', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " " + self.user.username + ' following ' + self.following.username + "."
