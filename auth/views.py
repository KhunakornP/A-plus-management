"""Module for redirecting users to authentication page."""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from urllib.parse import urljoin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
import requests
from django.urls import reverse
from django.contrib import messages
from rest_framework.views import APIView
import jwt
from time import sleep, time
from django.conf import settings


class GoogleOAuth2IatValidationAdapter(GoogleOAuth2Adapter):
    """Custom adapter for Google authentication."""

    def complete_login(self, request, app, token, response, **kwargs):
        """
        Override the complete_login method and make the iat check more lenient.

        This method stalls the server time until the token is ready to be
        validated. Then calls the allauth complete_login to validate the token.
        """
        try:
            delta_time = (
                jwt.decode(
                    response.get("id_token"),
                    options={"verify_signature": False},
                    algorithms=["RS256"],
                )["iat"]
                - time()
            )
        except jwt.PyJWTError as e:
            raise OAuth2Error("Invalid id_token during 'iat' validation") from e
        except KeyError as e:
            raise OAuth2Error("Failed to get 'iat' from id_token") from e

        # check if the iat is in the future and if it is within acceptable
        # difference, not the most elegant solution to this since
        # using a JS library to handle authentication would be better but,
        # it's the best I can do since we have no front end.
        if 0 < delta_time <= settings.ABSOLUTE_TOLERATED_TIME_DIFF:
            sleep(delta_time)
        else:
            print(delta_time)

        return super().complete_login(request, app, token, response, **kwargs)


class GoogleLoginCallback(APIView):
    """Class for handling token exchange between Google and Server."""

    def get(self, request, *args, **kwargs):
        """
        Get the access code from Oauth and exchange it for a  Google Token.

        After getting the token, this method saves the token to the database
        and authenticates the user.
        """
        code = request.GET.get("code")

        if code is None:
            messages.error(request, "Google sign in failed: Please login again.")
            #  change this to the login page after it is created as well
            return redirect(reverse("manager:taskboard_index"))

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
            request,
            user,
            backend="allauth.account.auth_backends.AuthenticationBackend",
        )
        return redirect(reverse("manager:taskboard_index"))

class GoogleLogin(SocialLoginView):
    """Social Login View for Google OAuth."""

    adapter_class = GoogleOAuth2IatValidationAdapter
    callback_url = settings.GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
