"""A view to create default roles upon user creation."""

from manager.models import StudentInfo

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_default_info_on_user_creation(sender, instance, created, **kwargs):
    """
    Create and bind a StudentInfo object whenever a new User is created.

    The default displayed name of the user is their Google email.
    :param sender: The Model class that is sending the signal.
    :param instance: The object that is being saved.
    :param created: A boolean, True if the created object is new.
    """
    if created:
        StudentInfo.objects.create(user=instance, displayed_name=instance.email)
