## Setting up Google OAuth 2.0

1. Go to [google cloud console](https://console.cloud.google.com/)
2. Login with your desired Google account
    - If you are using a new personally account you will need to link a payment method to the account.
    - If your Google account is associated with an organization you must create your project under that organization.
3. Create a new project
4. Fill in the form to create the project
5. Select the project from the dropdown
6. Create a consent screen in API and Services
7. Select user type to be external
8. Fill out the required fields:
   - App name
   - User support email
   - Developer contact information
   - Don't forget to click save and continue
9. Select scopes: email and profile then scroll down and update scope
10. Select the credentials tab and click create credentials, select Oauth client
11. Select Web application as the application type and fill in the name
12. Add `http://127.0.0.1:8000` to Authorised JavaScript origins
13. Add `http://127.0.0.1:8000` and `http://127.0.0.1:8000/accounts/google/login/callback/` to Authorised redirect URIs and save
14. Save the client id and secret and add them to your .env file
    - If you forget your client id and secret click on the app name in credentials to view them again.
