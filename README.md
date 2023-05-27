# Backend_task_Convin
## Task
- /rest/v1/calendar/init/ -> GoogleCalendarInitView()
This view should start step 1 of the OAuth. Which will prompt user for
his/her credentials
- /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
This view will do two things
1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar

## Result
![Result](https://github.com/Sreetama2001/Backend_task_Convin/assets/73426684/52077e62-f936-4719-8414-f57154359b92)
