'''
Created on 2016 jún. 2

@author: Balázs
'''

from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>-<int:age>')
def show_user_profile(username, age):
    # show the user profile for that user
    return 'User %s with age %s' % (username, str(age)) 

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
