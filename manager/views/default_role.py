"""A view to create default roles upon user creation."""

from django.contrib.contenttypes.models import ContentType
from manager.models import StudentInfo, ParentInfo, UserPermissions
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect, reverse


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


class UserSetupView(TemplateView):
    """A view for the user to select their 'role'."""

    template_name = "manager/account_creation.html"

    def get(self, request, *args, **kwargs):
        """
        Override the GET request and check if the user has set up their account.

        Redirect the user to the main page if they already have.
        """
        # check if user is logged in
        if not self.request.user.is_authenticated:
            return redirect(reverse("manager:main_login"))
        # check if user has already set up their account
        if self.request.user.has_perm("manager.is_verified"):
            return redirect(reverse("manager:taskboard_index"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Set up the user's account information based on the given fields."""
        # check if user is logged in
        if not self.request.user.is_authenticated:
            return redirect(reverse("manager:main_login"))
        # check if user has already set up their account
        if self.request.user.has_perm("manager.is_verified"):
            return redirect(reverse("manager:taskboard_index"))
        content_type = ContentType.objects.get_for_model(UserPermissions)
        verified = Permission.objects.get(codename="is_verified",
                                             content_type=content_type)
        parent = Permission.objects.get(codename="is_parent",
                                             content_type=content_type)
        calc_access = Permission.objects.get(codename="is_taking_A_levels",
                                             content_type=content_type)
        if request.POST["type"] == "parent":
            info = StudentInfo.objects.get(user=self.request.user)
            new_info = ParentInfo.objects.create(
                user=self.request.user, displayed_name=info.displayed_name
            )
            info.delete()
            new_info.save()
            self.request.user.user_permissions.add(verified)
            self.request.user.user_permissions.add(parent)
            self.request.user.user_permissions.add(calc_access)
            return redirect(reverse("manager:taskboard_index"))
        # if user is not a parent then they are a student
        # check if they take the A-levels
        if request.POST["exam"]:
            self.request.user.user_permissions.add(calc_access)
        self.request.user.user_permissions.add(verified)
        return redirect(reverse("manager:taskboard_index"))


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
