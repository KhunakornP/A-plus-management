"""Module for redirecting users to authentication page."""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from urllib.parse import urljoin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GoogleLoginCallback(APIView):
    """Class for handling token exchange between Google and Server."""

    def get(self, request, *args, **kwargs):
        """
        Get the access code from Oauth and exchange it for a  Google Token.

        After getting the token, this function saves the token to the database
        and authenticates the user.
        """
        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        params = {
            "process": "login",
        }

        response = requests.post(
            url=token_endpoint_url, data={"code": code}, params=params
        )
        key = response.json()["key"]
        user_id = Token.objects.get(key=key).user_id
        user = User.objects.get(pk=user_id)
        login(
            request, user, backend="allauth.account.auth_backends.AuthenticationBackend"
        )
        return redirect(reverse("manager:taskboard_index"))


class GoogleLogin(SocialLoginView):
    """Social Login View for Google OAuth."""

    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/auth/google-oauth2/callback/"
    client_class = OAuth2Client
