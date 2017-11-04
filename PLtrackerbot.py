import json #parse the JSON responses from Telegram into Python dictionaries so that we can extract the pieces of data that we need
import requests #make web requests using Python and we'll use it to interact with the Telegram API (similarly to what we were using our web browser for earlier). 
import time
import urllib
from dbhelper import DBHelper
from aftership import aftership_track


db = DBHelper()
track = aftership_track()

TOKEN = "471824003:AAH2AsNzhTtciPYtG6PL_NWxxyYzxCwL09A" #define our Bot's token that we need to authenticate with the Telegram API
URL = "https://api.telegram.org/bot{}/".format(TOKEN) #we create the basic URL that we'll be using in all our requests to the API.

#downloads the content from a URL and gives us a string.
def get_url(url): 
	response = requests.get(url) 
	content = response.content.decode("utf8") #or extra compatibility as this is necessary for some Python versions on some platforms
	return content

#gets the string response as above and parses this into a Python dictionary using json.loads()
def get_json_from_url(url):
	content = get_url(url) #from get_url
	js = json.loads(content) #from import json
	return js #return JSON

#calls the same API command that we used in our browser earlier, and retrieves a list of "updates" 
#to retrieve messages sent to our Bot using https://api.telegram.org/bot<your-bot-token>/getUpdates, and get JSON response
#The two pieces of information that we'll focus on for now are the chat ID, which will allow us to send a reply message and the message text which contains the text of the message.

def get_updates(offset=None):
	url = URL + "getUpdates"
	if offset:
		url += "?offset={}".format(offset)#we'll pass it along to the Telegram API to indicate that we don't want to receive any messages with smaller IDs than this
	js = get_json_from_url(url) #from def get_json_from_url(url)
	return js #return JSON


#calculates the highest ID of all the updates we receive from getUpdates.
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

#loop through each update and grab the text and the chat components so that we can look at the text of the message we received and respond to the user who sent it.
def handle_updates(updates):
    for update in updates["result"]:
		text = update["message"]["text"] #grab text
		chat = update["message"]["chat"]["id"] #grab chat component
		items = db.get_items(chat)
        
		#start
		if text == "/start":
			send_message("Welcome to PosLaju tracker. Sent a tracking number to be tracked.", chat)
			
		#other text starts with '/' just continue
		#elif text.startswith("/"): 
        #    continue
		
		#track tracking number
		elif text == "/add":
			add_new_tracking_number() #call this function
		
		#track existing number
		elif text == "/track":
			 track_tracking_number()
		
		#delete
		elif text == "/delete": 
			delete_tracking_number()

		else:
			add_new_tracking_number(text, chat)
			#db.add_item(text, chat)
            #items = db.get_items(chat)
            #message = "\n".join(items)
            #send_message(message, chat) #send back the text, with chat id?

#----------add and create tracking start---------------#			
def add_new_tracking_number():
	send_message("Add new tracking number.", chat)
	main() #get new text #macam salah
	add_new_tracking_number(text, chat)
	

def add_new_tracking_number(text, chat):
	db.add_item(text, chat)
	items = db.get_items(chat)
	track.create_track(text)

#----------add and create tracking end---------------#

#----------track tracking start---------------#			
def track_tracking_number():
	keyboard = build_keyboard(items) #from def build_keyboard #display saved items on keyboard
	send_message("Select an item to track", chat, keyboard)
	result = track.get_track(text)
	send_message(result["title"])


#----------track tracking end---------------#


#----------delete tracking start---------------#			
def delete_tracking_number():
	keyboard = build_keyboard(items) #from def build_keyboard #display saved items on keyboard
    send_message("Select an item to delete", chat, keyboard)
	db.delete_item(text, chat)
	track.delete_track(text)

#----------delete tracking end---------------#

#get the chat ID and the message text of the most recent message sent to our Bot. 
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


#takes the text of the message we want to send (text) and the chat ID of the chat where we want to send the message (chat_id). It then calls the sendMessage API command, passing both the text and the chat ID as URL parameters, thus asking Telegram to send the message to that chat.
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text) #able to reply to all of these messages (and pretty much anything else you throw at it, including emoji) flawlessly
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id) #from def get_updates
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1 #from def get_last_update_id
            handle_updates(updates) #from def handle_updates
        time.sleep(0.5)

#bring everything we have written together to actually receive and send a message
if __name__ == '__main__':
    main()
	
#First, we get the text and the chat ID from the most recent message sent to our Bot. 
#Then, we call send_message using the same text that we just received, effectively "echoing" the last message back to the user.