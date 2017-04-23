#this file will contain all the confiruation keys
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#this class holds all the needed configurations for the application
class BaseConfigurations(object):
	TEMPLATES_AUTORELOAD=True
	SECRET_KEY=os.environ.get('SECRET_KEY')
	MONGO_DBNAME='hackRU'
	MONGO_URI='mongodb://localhost:27017/hackRU'
	

def configure(app):
	app.config.from_object(BaseConfigurations)
	app.config['account_sid']=os.environ.get('TWILIO_ACCOUNT_SID')
	app.config['auth_token']=os.environ.get('TWILIO_AUTH_TOKEN')
	app.config['GOOGLE_KEY']=os.environ.get('GOOGLE_KEY')