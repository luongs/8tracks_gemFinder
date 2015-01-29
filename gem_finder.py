import requests
import json
import operator
import os 
import collections
import cgi
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

'''
Author: Sebastien Luong
Description: App queries the 8tracks API for mixes according to genre
			 and certification levels (Diamond, platinum, gold, gem)
'''

# Detect if environment is run locally or on heroku
if os.environ.get('HEROKU') is None: 
	# Instance is set for development code (local)
	app = Flask(__name__, instance_relative_config=True)	
else:
	# Instance is disabled for production code (ie: on heroku) 
	app = Flask(__name__, instance_relative_config=False)

# Load the default configuration
app.config.from_object('config')

#Load the configuration from the instance folder
app.config.from_pyfile('config.py')

if os.environ.get('HEROKU') is None: 
	# Retrieve API key from local config file
	api = app.config['API_KEY']	
else:
	# Retrieve API key from heroku config vars
	api = os.environ.get('API_KEY')	
	# Set SECRET_KEY from heroku
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')	

def escape_html(s):
    return cgi.escape(s, quote=True)

@app.route('/', methods=['GET','POST'])
def show_index():
	"""
	Initializes data structures with user response from webpage.
	Calls search_mix() to populate dictionary and returns results
	in html page. 
	"""
	result = None
	dictionary_list = []
	sorted_dictionary_list = []
	gemList_query = []
	popular_tag_list = []
	tags_query = ''
	# Give choice to search through popular or trending		
	if request.method == 'POST':
		# Update input boxes with latest data
		session.clear()
		# Get input request
		gemList_query = request.form.getlist('certification')
		tags_query = request.form['queryBox']
		tags_query = escape_html(tags_query)
		session['gem'] = gemList_query
		# Returns format that can be displayed on session
		session['query'] = tags_query.lower().replace(" ","_")
		dictionary_list = search_mix(tags_query,gemList_query)
		# Sorts dictionary in terms of gem value
		sorted_dictionary_list = sorted(dictionary_list, key = operator.itemgetter('likes_count'), reverse = True)
	else:
		popular_tag_list = get_popular_tags()
	return render_template('index.html', dictionary_list = sorted_dictionary_list, popular_tag_list = popular_tag_list, session = session)


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    return render_template('sitemap.xml')


def get_popular_tags():
	"""
	Returns five random tag suggestions to be displayed on index page
	"""
	popular_tag_list = []
	random_tag_list = []
	top_tag_url = 'http://8tracks.com/tags.json?api_key='+api+'?api_version=3'
	r = requests.get(top_tag_url)
	r.text
	json_result = json.loads(r.text)
	for tag_cloud in json_result['tag_cloud']['tags']:
		popular_tag_list.append(tag_cloud['name'])
	# Return a randomized list of the top 5
	random_tag_list = random.sample(popular_tag_list, 5)
	return random_tag_list 


def search_mix(tags_query,gemList_query): 
	"""
	Queries 8tracks API using user input genre and certification level.
	"""
	dictionary_list = []
	if tags_query and gemList_query:
		MAX_PAGE = 10
		FILTER = "popular"
		# 8tracks API only accepts space as underscores 
		tags_query = tags_query.lower().replace(" ","_")
		
		# Detect if 'gem' has been picked from list
		for gem in gemList_query:
			if gem=='gem':
				MAX_PAGE = 20
				FILTER = "trending"

		for i in range(1,MAX_PAGE):
			mix_url = "http://8tracks.com/mix_sets/tags:"+tags_query+\
						":"+FILTER+".json?include=mixes[likes_count]&page="+str(i)+\
						"&api_key="+api+'&api_version=3'
			r = requests.get(mix_url)
			r.text
			json_result = json.loads(r.text)
			if(int(r.headers['x-requests-left'])<30):
				print("Warning: "+r.headers['x-requests-left']+"left" )
			elif(int(r.headers['x-requests-left'])<20):
				print("Aborting calls, not enough API requests left") 
				break
			for gem in gemList_query:	
				for results in json_result['mix_set']['mixes']:
					if (results['certification']==gem):
						# Use ordered dictionary to retrieve keys in the same order they were added 
						mix_dictionary = collections.OrderedDict()
						# List must be used to hold both path and image link
						image_path =[results['path'], results['cover_urls']['sq133']]
						mix_dictionary['img_path'] = image_path		
						mix_dictionary['name'] = results['name']
						mix_dictionary['certification'] = results['certification']
						mix_dictionary['likes_count'] = results['likes_count']
						dictionary_list.append(mix_dictionary)
	# List is empty
	if not dictionary_list:
		mix_dictionary = collections.OrderedDict()
		mix_dictionary['name'] ='-'
		mix_dictionary['certification'] = '-'
		mix_dictionary['likes_count'] = 0
		mix_dictionary[''] = 'No mixes found! Try again with different tags or certifications'
		dictionary_list.append(mix_dictionary)
	return dictionary_list

if __name__ == '__main__':
	app.run()
