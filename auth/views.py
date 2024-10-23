"""Module for redirecting users to authentication page."""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from urllib.parse import urljoin, urlparse, parse_qs
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def extract_access_token_from_url(url):
    """"""
    parsed_url = urlparse(url)
    query_set = parse_qs(parsed_url.query)
    return query_set


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """Callback for exchanging Google Tokens."""

        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("http://localhost:8000",
                                     reverse("google_login"))
        params = {
            'process' : 'login',
        }

        response = requests.post(url=token_endpoint_url, data={"code": code}, params=params)
        key = response.json()["key"]
        user_id = Token.objects.get(key=key).user_id
        user = User.objects.get(pk=user_id)
        login(request, user,
              backend="allauth.account.auth_backends.AuthenticationBackend")
        return redirect(reverse("manager:taskboard_index"))


class GoogleLogin(SocialLoginView):
    """Social Login View for Google OAuth."""

    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/auth/google-oauth2/callback/"
    client_class = OAuth2Client