# CalendarTrackerBot
This was a project created as a means for users to store Reminders and Events on Telegram.

How to use:
This script was written in Python3. Input your own key and run the script as given.
This bot is created to allow users and groups to store timed reminders and events all on Telegram for easy access. 

Default commands:
/start: Initialising the bot
/help: Give helpful information about the bot
/display : display the current reminders and events recorded

Instructions:
- To store a reminder:
  ‘remind <space>(date in ddmmyy format)<space>(time in 2359 format)<space>(Reminder name)’.
  Eg. remind 191118 0800 Buy Breakfast
  
- To store an event:
  ‘event<space>(date in ddmmyy format)<space>(time in 2359 format)<space>(Event name).
  Eg. ‘event 191118 0800 Fetch Timmy from school’
  Events are special in a way that they time inputs are optional. Some events are throughout the day and this is what makes events 
  different from reminders.
  Eg.‘event today Timmy’s 21st Birthday’
  
- To delete and event or reminder:
  You can delete events or reminders that you have no use for. Just type in the following format:
  ‘delete<space>reminder/event<space>corresponding number’.
  Eg ‘delete event 1’
  Eg 'delete reminder 1'

Notes:
- The difference between events and reminders are that reminders will send an automated message when the given timing has passed. 
- Events do not need a specific time as we understand that some events are throughout them day
- All events and reminders are sorted accordingly upon creating a new one
- Instead of dates, inputs of 'today' and 'tomorrow' are excepted and the respective dates will automatically be logged
- Time tracking is all done in unix time, not system time.
- Please contribute to the making of this bot to make it better!
