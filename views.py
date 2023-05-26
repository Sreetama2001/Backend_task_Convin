from django.http import HttpResponseRedirect, JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.shortcuts import render
import os
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))

secret_file_path = os.path.join(current_dir, 'secret.json')
flow = Flow.from_client_secrets_file(
    secret_file_path,
    scopes=['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar'],
    redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
)
def home(request):
    return render(request, 'home\home.html')

def CalenderInitView(request):
    state =None
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['google_auth_state'] = state
    return HttpResponseRedirect(authorization_url)


# def CalenderRedirectView(request):
#     print("Authorizing ..... ")
#     state = request.session.pop('google_auth_state', None)
#     print("  the state now is " , state)
#     if state is None:
#         return JsonResponse({'error': 'Authorization state not found.'}, status=400)

#     authorization_response = request.build_absolute_uri()
#     try:
#         flow.fetch_token(authorization_response=authorization_response)
#         credentials = flow.credentials

#         service = build('calendar', 'v3', credentials=credentials)
#         events_result = service.events().list(calendarId='primary', maxResults=10).execute()
#         events = events_result.get('items', [])

#         return JsonResponse({'events': events})
#     except OAuth2Error as e:
#         return JsonResponse({'error': 'Unauthorized access, user must authorize first , the error is : ' + str(e)}, status=401)
def CalenderRedirectView(request):
    logger = logging.getLogger(__name__)
    logger.debug("Authorizing...")

    state = request.session.pop('google_auth_state', None)
    logger.debug("The state now is: %s", state)

    if state is None:
        logger.error("Authorization state not found.")
        return JsonResponse({'error': 'Authorization state not found.'}, status=400)

    authorization_response = request.build_absolute_uri()
    try:
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        return JsonResponse({'events': events})
    except OAuth2Error as e:
        logger.exception("OAuth2Error occurred: %s", e)
        return JsonResponse({'error': 'Unauthorized access, user must authorize first. Error: ' + str(e)}, status=401)
