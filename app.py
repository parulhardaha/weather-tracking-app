import os
from flask import Flask, render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import requests

# 1. set up db config
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app) # instance taht is linked with flask

#2. create table-model
#weather model
class Weather(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    city=db.Column(db.String(50),nullable=True)
    main=db.Column(db.String(50))
    temp=db.Column(db.Float)
    feels_like=db.Column(db.Float)
    dt=db.Column(db.Integer)

#3. initalie and create table
with app.app_context():
    db.create_all()
   
@app.route('/')
def home():
  return render_template("home.html")

@app.route('/result',methods=['GET'])
def result():
  #get city 
  city=request.args.get('city')

  api_key='2ae9bd609aa084fec4d1e35ec1244b22'
  api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'


  #send req to weather app
  response=requests.get(api_url)

  if response.status_code==200:
     #converted into python dict
     weather_data=response.json()
  else:
     weather_data=None       
  return render_template("summary.html",data=weather_data,city=city)

