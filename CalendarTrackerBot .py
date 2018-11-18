#! /usr/bin/python3

import telepot
import json
import requests
import time
import urllib
import datetime

TOKEN = ***INSERT API KEY HERE***
bot = telepot.Bot(TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Returns the contents of the URL 
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# Returns the contents of the URL, but in json format
# Seems like the same as get_url so far, but just more spaced out.
# Main diff is boolean returns here are True instead of true (Better for python3)
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# Converts datetime in the format of '08102018 1300' into unix time
def datetime_to_unix(userDate, userTime):
    s = userDate + ' ' + userTime
    unix_time = time.mktime(datetime.datetime.strptime(s, "%d%m%Y %H%M").timetuple())
    return unix_time

# Returns updates 
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=0"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_sticker(file_id, chat_id):
    text = urllib.parse.quote_plus(file_id)
    url = URL + "sendSticker?sticker={}&chat_id={}".format(text, chat_id)
    print (url)
    get_url(url)

userDict = {}

instruction = '''⚠️ INSTRUCTIONS ⚠️
\n✅ Set Events & Reminders
- To set a new event or reminder, type \'remind\' or \'event\' followed by date (DDMMYY), time (HHMM) and your text
(e.g. Event 021218 1400 Lunch with mum OR Remind today 1330 Buy eggs)
*Please key in your time in 24-hour format*
*'Today' and 'Tomorrow' are both accepted as date stamp*
\n❇️ Display Events & Reminders
- Type /events to display your list of Events
- Type /reminders to display your list of Reminders
- Type /display to display your list of BOTH Events and Reminders
\n❎ Delete Events & Reminders
- Type 'delete' followed by 'event' or 'reminder' and its assigned number on the list
(e.g. Delete event 2)
\n✨ For feedback on this bot, please contact creators @willistayy or @shanecsj.'''

def showEvents(userid):
    lstEvent = userDict[userid]['events']
    label = 1
    eventLst = 'Your Current Events are as follows: \n'
    if len(lstEvent) == 0:
        return 'You currently have no events to display. \n'

    else:
        for item in lstEvent:
            if len(item) == 4:
                date1 = datetime.datetime.fromtimestamp(int(item[3]))
                date2 = date1.strftime("%d %b")
                eventLst = eventLst + str(label) + '. ' + item[2] + ' on ' + date2 +'\n'
                label = label + 1
            else:
                date1 = datetime.datetime.fromtimestamp(int(item[4]))
                date2 = date1.strftime("%d %b")
                eventLst = eventLst + str(label) + '. ' + date2 + ' - ' + item[3] + '  (' + item[2] + ' hrs) \n'
                label = label + 1
    return eventLst

def showReminders(userid):
    lstRem = userDict[userid]['reminders']
    label = 1
    remLst = 'Your Current Reminders are as follows: \n'
    if len(lstRem) == 0:
        return 'You currently have no reminders to display'
    
    else :
        for item in lstRem:
            date1 = datetime.datetime.fromtimestamp(int(item[4]))
            date2 = date1.strftime("%d %b")
            remLst = remLst + str(label) + '. ' + date2 + ' (' + item[2] + ' hrs) ' + item[3] + '\n'
            label = label + 1
    return remLst

def isPrivate(update):
    if update['message']['chat']['type'] == 'private':
        return True
    else:
        return False

def isTime(timetext):
    try:
        time.strptime(timetext, '%H%M')
        return True
    except:
        return False

def isDate(datetext):
    try:
         datetime.datetime.strptime(datetext, '%d%m%Y')
         return True
    except:
        return False

def isInteger(x):
    try:
        x = int(x)
        return True
    except:
        return False

def deleteItem(userid, itemType, pos):
    itemList = userDict[userid][itemType]
    if pos <= len(itemList):
        del itemList[pos - 1]

        if itemType == 'events':
            send_message('Successfully deleted event', userid)
            send_message(showEvents(userid), userid)
        elif itemType == 'reminders':
            send_message('Successfully deleted reminder', userid)
            send_message(showReminders(userid), userid)
    else:
        send_message('There is no such event to delete', userid)
    


def processUpdates(updates):
    for update in updates['result']:
        # Get user ID
        userid = update['message']['chat']['id']
        
        # Get context and split them up by the first 3 spaces
        context = update['message']['text']
        print(str(userid) + ': ' + context)

        # If userid not in our dictionary, create a new one
        if userid not in userDict:
            userDict[userid] = {'reminders': [], 'events': []}

        # Mandatory initialisation of the bot
        if context == '/start' or context == '/start@CalendarTrackerBot':
            send_sticker('CAADAgADtA0AAomufxHtCZWJR8EQxwI', userid)
            send_message('Welcome fellow user \nType /help for the instructions to use this bot', userid)

        # /help command
        elif context == '/help' or context == '/help@CalendarTrackerBot':
            send_message(instruction, userid)

        # /display_all command
        elif context == '/display' or context == '/display@CalendarTrackerBot':
            send_message(showEvents(userid) + '\n' + showReminders(userid), userid)

        # /display_events command
        elif context == '/events' or context == '/events@CalendarTrackerBot':
            send_message(showEvents(userid), userid)

        # /display_reminders command
        elif context == '/reminders' or context == '/reminders@CalendarTrackerBot':
            send_message(showReminders(userid), userid)

        elif 'good night' in context.lower():
            send_message('Good night sonny', userid)

        else:
            # Split context into first 3 spaces
            event_time_context = context
            context = context.split(' ', 3)
            
            # Delete function
            if context[0].lower() == 'delete':
                if (len(context) < 3 and isPrivate(update)):
                    send_message('Invalid delete command', userid)
                    pass
                
                # Check second word is 'event' and third word is a digit
                if (context[1].lower() == 'event' and isInteger(context[2])):
                    pos = int(context[2])
                    deleteItem(userid, 'events', pos)
                # Check second word is 'reminder' and third word is a digit
                elif (context[1].lower() == 'reminder' and isInteger(context[2])):
                    pos = int(context[2])
                    deleteItem(userid, 'reminders', pos)
                # If it's a private chat, send error message
                elif isPrivate(update):
                    send_message('Invalid delete command', userid)
                    pass
                # If it's a group chat, ignore and pass
                else:
                    print('Group DELETE error passed')
                    pass
                
            # Add Event function
            elif context[0].lower() == 'event':
                if (len(context) < 3 and isPrivate(update)):
                    send_message('Invalid event command', userid)
                    pass
                
                if context[1].lower() == 'today':
                    ts = time.time()
                    context[1] = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y')
                elif context[1].lower() == 'tomorrow':
                    ts = time.time() + 86400
                    context[1] = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y')
                elif isInteger(context[1]) and len(context[1]) == 6:
                    context[1] = context[1][:4] + '20' + context[1][4:]

                if isDate(context[1]) and isTime(context[2]):
                    unix = datetime_to_unix(context[1], context[2])
                    if unix < time.time():
                        send_message('Don\'t live in the past, son', userid)
                        pass
                    else:
                        context.append(unix)
                        userDict[userid]['events'].append(context)
                        userDict[userid]['events'] = sorted(userDict[userid]['events'], key = lambda x:x[-1])
                        send_message('Event successfully added', userid)

                elif context[1].lower() == 'yesterday':
                    send_message('Yesterday is history\nTomorrow is a mystery\nToday is a gift', userid)
                    pass
                
                elif isInteger(context[1]) and isDate(context[1]) == False:
                    send_message('Invalid date format', userid)
                    pass

                elif isInteger(context[2]) and isTime(context[2]) == False:
                    send_message('Invalid time format',userid)
                    pass

                # ****Private create event without time****
                elif isDate(context[1]) and not isTime(context[2]):
                    date_ = context[1]
                    context = event_time_context.split(' ', 2)
                    context[1] = date_
                    unix = datetime_to_unix(context[1], '2359')
                    context.append(unix)
                    userDict[userid]['events'].append(context)
                    userDict[userid]['events'] = sorted(userDict[userid]['events'], key = lambda x:x[-1])
                    send_message('Event successfully added', userid)
                
                elif isPrivate(update):
                    send_message('Invalid event command', userid)
                    pass
                
                else:
                    print('Group EVENT error passed')
                    pass

            # Add Reminder function
            elif context[0].lower() == 'remind':
                if (len(context) < 3 and isPrivate(update)):
                    send_message('Invalid remind command', userid)
                    pass

                if context[1].lower() == 'today':
                    ts = time.time()
                    context[1] = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y')
                elif context[1].lower() == 'tomorrow':
                    ts = time.time() + 86400
                    context[1] = datetime.datetime.fromtimestamp(ts).strftime('%d%m%Y')
                elif isInteger(context[1]) and len(context[1]) == 6:
                    context[1] = context[1][:4] + '20' + context[1][4:]

                if isDate(context[1]) and isTime(context[2]):
                    print('is date and time')
                    unix = datetime_to_unix(context[1], context[2])
                    if unix < time.time():
                        send_message('Don\'t live in the past, son', userid)
                        pass
                    else:
                        context.append(unix)
                        userDict[userid]['reminders'].append(context)
                        userDict[userid]['reminders'] = sorted(userDict[userid]['reminders'], key = lambda x:x[-1])
                        send_message('Reminder successfully added', userid)

                elif context[1].lower() == 'yesterday':
                    send_message('Yesterday is history\nTomorrow is a mystery\nToday is a gift', userid)
                    pass

                elif isInteger(context[1]) and isDate(context[1]) == False:
                    send_message('Invalid date format')
                    pass

                elif isInteger(context[2]) and isTime(context[2]) == False:
                    send_message('Invalid time format')
                    pass

                elif isPrivate(update):
                    send_message('Invalid reminder command', userid)
                    pass

                else:
                    print('Group REMINDER error passed')
                    pass

            else:
                if isPrivate(update):
                    send_sticker('CAADAgADtAIAAog4OAJFrHKuSg7HDQI' ,userid)
                    send_message('Please enter a valid input', userid)
                    pass
                else:
                    print('Group error passed')
                    pass

                        	
def main():
    last_update_id = None
    while True:
        currtime = time.time()
        print(userDict)
        for userKey in list(userDict.keys()):
            for rem in userDict[userKey]['reminders']:
                if rem[-1] < currtime:
                    send_message(rem[3], userKey)
                    userDict[userKey]['reminders'].remove(rem)

            for ev in userDict[userKey]['events']:
                if ev[-1] < currtime:
                    print('Event has passed. Deleting event.')
                    userDict[userKey]['events'].remove(ev)
                    
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            try:
                processUpdates(updates)
            except:
                print('pass')
                pass
        time.sleep(1)

if __name__== '__main__':
    main()
