#import flask and other classes from falsk
from flask import Flask,render_template
from flask_bootstrap import Bootstrap


app=Flask(__name__)

#loading configuraitons from config.py
app.config.from_object('config')


Bootstrap(app)

@app.route('/')
def home():
	return render_template('index.html')


