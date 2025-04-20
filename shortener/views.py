import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging

# Set up logging
logger = logging.getLogger(__name__)

API_URL = "http://194.242.56.190:8000"
EMAIL = "test123@example.com"
PASSWORD = "securepassword123"

@csrf_exempt
def shorten_view(request):
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.POST.get("url")
        if not original_url:
            error = "URL is required."
            return render(request, "form.html", {"error": error})

        # 1. Login
        login_data = {"email": EMAIL, "password": PASSWORD}
        login_res = requests.post(f"{API_URL}/auth/login", json=login_data)

        if login_res.status_code != 200:
            error = "Login failed"
        else:
            token = login_res.json().get("access_token")
            logger.info(f"Received token: {token}")  # Log the token

            # 2. Shorten
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            shorten_data = {"original_url": original_url}
            logger.info(f"Sending shorten request: {shorten_data}")  # Log the request data
            shorten_res = requests.post(f"{API_URL}/shorten", json=shorten_data, headers=headers)

            if shorten_res.status_code == 200:
                # Access the short_code from the response and construct the shortened URL
                short_code = shorten_res.json().get("short_code")
                short_url = f"{API_URL}/{short_code}"
            else:
                error = f"URL shortening failed. Status Code: {shorten_res.status_code}"
                logger.error(f"Error response: {shorten_res.text}")  # Log the error response

    return render(request, "form.html", {"short_url": short_url, "error": error})
