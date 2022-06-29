from  .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            name = user.username,
            email = user.email,
            username = user.first_name,
        )

post_save.connect(createProfile,sender=User)