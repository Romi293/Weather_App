from flask import Flask, render_template, request, json, session, redirect, url_for
import os
from modules.api_calls import api_request
from datetime import timedelta
import urllib.request
import requests

"""
Weather App with Flask and Jinja

This Flask web application provides a user interface to retrieve weather information
for any location globally. Users can access the app through three main functionalities:

* Login Screen: Allows users to authenticate as an exist users
* Signup Screen: Enables new user registration
* Weather Screen: Displays the 7-day weather forecast for a specific location given by the user

App features:

* User authentication (login/signup)
* Weather API integration to fetch location-specific forecasts
* 7-day weather forecast display
"""


app = Flask(__name__)

app.secret_key = "RomiSecretKey"
app.permanent_session_lifetime = timedelta(seconds=20)

################################################################

def is_alpha(location):
    '''Checks if there are special characters or digits and deletes spaces'''
    return location.replace(" ", "").isalpha() 

 
def valid_length(location):
    '''Checks if the location input length is valid'''
    return (len(location) >= 1) and (len(location) <= 10)


@app.route('/get_weather', methods = ['POST', 'GET'])
def get_weather():
    '''The function checks if the location input from the user is valid
       and sends an API request to get the weather in this location'''
    if 'username' not in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        location = request.form.get("CityName")
        if is_alpha(location) and valid_length(location):
            resp = api_request(location)
            if resp:
                return render_template('index.html', resp=resp)
            else:
                return render_template('index.html', invalid_location=location)    
        else:
            return render_template('index.html', invalid_location=location)
    return render_template('index.html')

################################################################

@app.route('/')
def render_default(): 
    '''This function renders the default page in the web app which is the login html file.
    If the user is in the session, it will lead him inside the app to select a location to check the weather'''
    if 'username' in session:
        return redirect(url_for("get_weather"))
    return redirect(url_for("login"))


@app.route("/login", methods = ['POST', 'GET'])
def login():
    '''A function that retrieves a username and password from the login html file
    and checks if the details exists in the users json file.
    The function shows appropriate message if the details not exist in the file,
     or let the user in the app directly into the weather screen'''
    if request.method == 'POST':
        username = request.form.get("UserName")
        password = request.form.get("Password")
        with open('users.json', "r") as file:
            json_data = json.load(file)

        for user in json_data['users']:
            if user['username'] == username and user['password'] == password:
                print("Welcome!")
                session['username'] = username
                return redirect(url_for('get_weather'))
            else:
                continue
        print("Your username or password are incorrect")
        return render_template("login.html", user_not_exist=username)
    return render_template("login.html")


@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    '''A function that retrieves username and password from the signup html file,
    checks if it exist in the the users json file and saves it in it if not.
    After that, the function leads the user to make a login'''
    new_username = request.form.get("new_username")
    new_password = request.form.get("new_password")
    if request.method == 'POST':
        print(new_username)
        print(new_password)
        with open('users.json', "r+") as f:            
            file = json.load(f)
            for user in file['users']:
                if user.get('username') == new_username:
                    print("exists")
                    return render_template("signup.html", user_already_exist=new_username)
                continue
            print("not exists")
            file['users'].append({
                'username': new_username, 
                'password': new_password
            })
            f.seek(0)
            file = json.dump(file, f, indent = 4)
        return redirect(url_for("login", success_signup=new_username))
    return render_template("signup.html")


@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    '''A function that closes the session of the user and leads him out of the app
    to the login screen'''
    session.pop('username', None)
    return redirect(url_for("login"))


######################################################

    
if __name__ == "__main__":
    app.run(port='8000', debug=True)
 

