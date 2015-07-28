from flask import Flask, redirect, render_template, request
import redis
import httplib
import hashlib
import base64
from urlparse import urlparse

r = redis.StrictRedis(host='localhost', port=8080, db=2)

'''
	Helper functions
'''

def generate_hash(url):
    """
    Generates the hash value to be stored as key in the redis database
    """
    hashval = base64.urlsafe_b64encode(hashlib.md5(url).digest())
    hashval=hashval[0:6]
    
    return hashval

def getoriginal(path):
	"""
	Returns the original url for a given key
	"""
	global r
	val = r.get(path)
	return val

def shorten(text=None):
	"""
	saves the shortened url in redis database along with 
	the original and returns the short
	"""
	global r,to
	url = urlparse(text)
	if url.scheme not in ["http","https"]:
		text="http://"+text
	short = generate_hash(text)
	r.set(short,text)
	return render_template('result.html',text="localhost:5000/"+short)

'''
	App starts from below
'''

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/',methods=['POST'])
def myform():
	text=request.form['code']
	result=shorten(text)	
	return result

@app.route('/<path:path>')
def catch_all(path):
	original = getoriginal(path)
	if original == None:
		return "404 not found"
	else:
		return redirect(original)



if __name__ == '__main__':
	app.run(port=5000)