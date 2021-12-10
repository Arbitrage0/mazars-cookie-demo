from flask import Flask, request, make_response, render_template
import os, binascii
import datetime

app = Flask('app')

@app.route('/', methods = ['GET', 'POST'])
def index():
  if request.method == 'POST': 
    resp = make_response("Cookies Cleared!")
    resp.set_cookie('session_visits', expires=0)
    #resp.set_cookie('tracking_id', expires=0)
    return resp
  elif request.cookies.get('session_visits') is None:
    resp = make_response(render_template('index.html', message="Welcome to this page for the first time!"))
    resp.set_cookie('session_visits', "1", httponly = True)
    if request.cookies.get('tracking_id') is None:
      resp.set_cookie('tracking_id', binascii.b2a_hex(os.urandom(10)), httponly = True, expires=datetime.datetime.now()+datetime.timedelta(days=180))
    return resp
  else: 
    c = int(request.cookies.get('session_visits'))
    c += 1
    resp = make_response(render_template('index.html', message="You have visted this page " + str(c) + " times!"))
    resp.set_cookie('session_visits', str(c), httponly = True)
    return resp

app.run(host='0.0.0.0', port=8080)
