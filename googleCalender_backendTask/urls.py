from django.contrib import admin
from django.urls import path
from views import CalenderInitView, CalenderRedirectView, home

urlpatterns = [
    path('', home, name='home'),
    path('rest/v1/calendar/init/', CalenderInitView, name='google-calendar-init'),
    path('rest/v1/calendar/redirect/', CalenderRedirectView, name='google-calendar-redirect'),
]

# request.build_absolute_uri(reverse('google-calendar-redirect'))