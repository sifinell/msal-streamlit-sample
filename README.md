# Azure AD Authentication in Streamlit

## Overview
This Streamlit application integrates Microsoft Azure Active Directory (Azure AD) authentication using the Microsoft Authentication Library (MSAL). Users can log in with their Microsoft accounts and retrieve basic profile information from Microsoft Graph API.

## Features
- Azure AD authentication with OAuth2.
- Secure token exchange using MSAL.
- Fetch and display user profile information from Microsoft Graph API.
- Logout functionality to clear session data.

## Authentication Flow
1. The user clicks the **Login with Microsoft** button.
2. The app redirects the user to Microsoft login.
3. After authentication, the app retrieves an access token.
4. The app uses the token to fetch user details from Microsoft Graph API.
5. The user can log out to clear their session.

## Code Structure
- **`msal_app = msal.PublicClientApplication(...)`**: Initializes the MSAL authentication client.
- **`msal_app.get_authorization_request_url(...)`**: Generates the Microsoft login URL.
- **Token Exchange**: Uses `acquire_token_by_authorization_code()` to retrieve the access token.
- **User Info Retrieval**: Calls `https://graph.microsoft.com/v1.0/me` to fetch user details.
- **Session Management**: Stores the token in `st.session_state` for authentication state management.

## Notes
- Ensure that the Azure AD app registration has **redirect URIs** properly configured.
- The **logout function** clears the session but does not invalidate the token on Microsoft’s end.
- This app uses **authorization code flow**, making it suitable for web applications.
