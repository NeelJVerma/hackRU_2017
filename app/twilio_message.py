
#After user sends image to the server, Twilio makes http request to 
#the server. If so, this function is called, which retries 
#data about the user's content from Twilio server
from twilio.rest import Client
import twilio.twiml

def get_message(database_handle):
	database_handle.askHer.insert(user_info)
	
	