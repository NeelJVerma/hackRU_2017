#import flask and other classes from falsk
from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from googleplaces import GooglePlaces, types, lang

from twilio.twiml.messaging_response import MessagingResponse

from . import config


#import twilio client object
#from . import twilio_message



app=Flask(__name__)

#load configuration to app.config using configure function in config.py
config.configure(app)


Bootstrap(app)
mongo=PyMongo(app)

@app.route('/index', methods=['GET','POST'])
def home():
	return render_template('index.html')




@app.route('/getMessage',methods=['GET','POST'])
def messages():
	resp=MessagingResponse()
	resp.message("Hello")
	user_info={
			'user_number':request.form['From'],
			'image':request.form.get('MediaU3rl0',None),
			'city':request.form['FromCity'],
			'zip_code':request.form['FromCity'],
			'country':request.form['FromCountry']
		}
	data = location_scrap('starbucks',request.form['FromCity'])
	
	mongo.db.askHer.insert_one(user_info)
	return str(resp)


def location_scrap(business_name,loc):
        #establishes connection to google's servers based on a valid auth key
        google_places = GooglePlaces('AIzaSyCC_weuF9RVrynjabaplRUgjpZyHuD2vuM')

        # You may prefer to use the text_search API, instead.
        query_result = google_places.nearby_search(location=loc, keyword=business_name,radius=20000, types=[types.TYPE_FOOD])
        # If types param contains only 1 item the request to Google Places API
        # will be send as type param to fullfil:
        # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

        if query_result.has_attributions:
                        print(query_result.html_attributions)
        data = []

        for place in query_result.places:
                place.get_details()
                # Returned places from a query are place summaries.
                reviews = []
                for review in place.details['reviews']:
                        review_data = {"text":review["text"],"rating":review["rating"],"time":review["time"]}
                        reviews.append(review_data)
                place_data = (place.name,place.rating,reviews)
                data.append(place_data)
        return data
