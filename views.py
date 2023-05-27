from django.http import HttpResponseRedirect, JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
from django.shortcuts import render
from django.urls import reverse
import os
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
secret_file_path = os.path.join(current_dir, 'secret.json')

def home(request):
    return render(request, 'home/home.html')

def CalenderInitView(request):
    flow = Flow.from_client_secrets_file(
        secret_file_path,
        scopes=['https://www.googleapis.com/auth/calendar.events'],
    )
    flow.redirect_uri = "http://localhost:8000/rest/v1/calendar/redirect/"

    authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent',include_granted_scopes='true')
    request.session['google_auth_state'] = state
    return HttpResponseRedirect(authorization_url)

def CalenderRedirectView(request):
    logger = logging.getLogger(__name__)
    logger.debug("Authorizing...")

    state = request.GET.get('state', None)
    if not state:
        state = request.session.pop('google_auth_state', None)
    if not state:
        return JsonResponse({'error': 'Authorization state not found.'}, status=400)
    
    logger.debug("The state now is: %s", state)

    flow = Flow.from_client_secrets_file(
        secret_file_path,
        scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar'],
    )
    flow.redirect_uri = 'http://' + request.get_host() + reverse('google-calendar-redirect')
    authorization_response = request.build_absolute_uri()
    if "http:" in authorization_response:
        authorization_response = "https:" + authorization_response[5:]
    try:
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
        }
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return JsonResponse({'events': events})
        # success_message = "Authorization successful!"
        # return render(request, 'other/success.html', {'message': success_message})
    except OAuth2Error as e:
        logger.exception("OAuth2Error occurred: %s", e)
        return JsonResponse({'error': 'Unauthorized access, user must authorize first. Error: ' + str(e)}, status=401)
