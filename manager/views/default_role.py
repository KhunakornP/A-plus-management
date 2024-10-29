"""A view to create default roles upon user creation."""

from manager.models import StudentInfo

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.conf import settings


class LoginView(TemplateView):
    """View for rendering the login page."""

    template_name = "manager/login.html"

    def get_context_data(self, **kwargs):
        """
        Override the context data to pass data to construct the login link.

        Pass the client_id and callback uri to construct the Google Oauth link.
        """
        context = super().get_context_data(**kwargs)
        context["callback_uri"] = settings.GOOGLE_CALLBACK_URI
        context["client_id"] = settings.GOOGLE_CLIENT_ID
        return context


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
