import streamlit as st
import msal
import requests
import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPES = ["User.Read"]  # Required permissions

# Initialize MSAL app
msal_app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

st.title("Azure AD Authentication in Streamlit")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# Step 1: Generate login URL
if st.session_state["access_token"] is None:
    login_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)

    if st.markdown(f'<a href="{login_url}" target="_self" style="text-decoration: none;"><button>Login with Microsoft</button></a>',
        unsafe_allow_html=True
    ):

        # Step 2: Handle Redirect (User comes back with a code)
        query_params = st.query_params
        if "code" in query_params:
            auth_code = query_params["code"]
            
            # Exchange code for token
            token_response = msal_app.acquire_token_by_authorization_code(auth_code, SCOPES, redirect_uri=REDIRECT_URI)

            if "access_token" in token_response:
                st.session_state["access_token"] = token_response["access_token"]
                
                st.rerun()
            else:
                if st.session_state["access_token"]:
                    st.error("Authentication failed. Please try again.")

# Step 3: Fetch User Info
if st.session_state["access_token"]:
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    user_info = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()

    st.success(f"Welcome {user_info['displayName']} ({user_info['mail']})")
    st.json(user_info)

    if st.button("Logout"):
        st.session_state["access_token"] = None
        st.rerun()