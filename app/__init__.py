#import flask and other classes from falsk
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from googleplaces import GooglePlaces, types, lang

from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime,timedelta

from . import config





app=Flask(__name__)

#load configuration to app.config using configure function in config.py
config.configure(app)


Bootstrap(app)
mongo=PyMongo(app)


#we will use context processing for sending live data to the server
#this makes a dictionary available to all the templates for use
BUSINESS_DATA=[]

@app.context_processor
def sendFeed():
	return dict(BUSINESS_DATA=BUSINESS_DATA)


@app.route('/getMessage',methods=['GET','POST'])
def home():
	if request.method=='POST':
		messages()

	return render_template('front_page.html')




#@app.route('/getMessage',methods=['GET','POST'])
def messages():
	resp=MessagingResponse()
	#resp.message("Hello")
	user_info={
			'user_number':request.form['From'],
			'image':request.form.get('MediaU3rl0',None),
			'city':request.form['FromCity'].lower(),
			'zip_code':request.form['FromZip'],
			'country':request.form['FromCountry'].lower()
		}
	#we will make BUSINESS_DATA a global variable to hold business data
	#either from an api or a database query
	global BUSINESS_DATA

	if checkDatabase('starbucks',user_info['city']):
		data=mongo.db.companies.find({"location":user_info['city'],"business":'starbucks'})
		for each_data in data:
			try:
				temp_data=(each_data['business'],each_data['avg_rating'],each_data['text'],each_data['location'])
				BUSINESS_DATA.append(temp_data)
			except KeyError:
				pass
		# #data['image']=user_info['image']
		# BUSINESS_DATA=[data]+BUSINESS_DATA
		# print(dict(BUSINESS_DATA))
	else:
		data = location_scrap('starbucks',user_info['city'])
		for each_data in data:
			try:
				temp_data=(each_data['business'],each_data['avg_rating'],each_data['text'],each_data['location'])
				BUSINESS_DATA.append(temp_data)
			except KeyError:
				pass
		mongo.db.askHer.insert_one(user_info)

		#iterate through each item (which is a dictionary) of data
		#and store it in the database
		for dicts in data:
			mongo.db.companies.insert_one(dicts)

	return str(resp)
	#return redirect(url_for('home'))


def location_scrap(business_name,loc):
	#establishes connection to google's servers based on a valid auth key
	google_places = GooglePlaces(app.config['GOOGLE_KEY'])

	# You may prefer to use the text_search API, instead.
	query_result = google_places.nearby_search(location=loc, keyword=business_name,radius=20000, types=[types.TYPE_FOOD])
	# If types param contains only 1 item the request to Google Places API
	# will be send as type param to fullfil:
	# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html
	data = []	#this list will hold a bunch of dictionaries
	for place in query_result.places:
		place.get_details()
		# Returned places from a query are place summaries.
		review_data={}
		for review in place.details['reviews']:
			N = 180
			date_N_days_ago = datetime.now() - timedelta(days=N)
			review_time = datetime.fromtimestamp(int(review['time']))
			if date_N_days_ago < review_time:
				#these are the information we will be taking from place.details object
				temp_data = {"text":review["text"],"rating":str(review["rating"]),"time":review["time"]}
				review_data.update(temp_data)

		#there are remaining data (out of the loop) which still 
		#needs to be added to the dictionary review_data
		review_data['location']=loc.lower()
		review_data['business']=place.name.lower()
		review_data['avg_rating']=str(place.rating)

		#now, the dictionary is filled,
		#before the review_data is reset, append it to the list data
		data.append(review_data)
	#print(data)
	return data


def checkDatabase(business,location):
	aa=mongo.db.companies.find_one({"location":location,"business":business})
	print(type(aa))
	if type(aa) is dict:
		return True
	else:
		return False
