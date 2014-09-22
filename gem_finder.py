from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json, operator, os

# Detect if environment is run locally or on heroku
if os.environ.get('HEROKU') is None: 
	app = Flask(__name__, instance_relative_config=True)	# instance is set for development code (local)
else: 
	app = Flask(__name__, instance_relative_config=False)	# instance is disabled for production code (ie: on heroku)

# Load the default configuration
app.config.from_object('config')

#Load the configuration from the instance folder
app.config.from_pyfile('config.py')

if os.environ.get('HEROKU') is None: 
	api = app.config['API_KEY']		# retrieve API key from local config file
else:
	api = os.environ.get('API_KEY')	# retrieve API key from heroku config vars
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

print(api)

@app.route('/', methods=['GET','POST'])
def show_index():
	result = None
	dictionary_list = []
	sorted_dictionary_list = []
	gemList_query = []
	tags_query = ''
	# give choice to search through popular or trending		
	if request.method == 'POST':
		# update input boxes with latest data
		session.clear()
		# get input request
		gemList_query = request.form.getlist('certification')
		tags_query = request.form['queryBox']
		session['gem'] = gemList_query
		session['query'] = tags_query.lower().replace(" ","_")		# returns format that can be displayed on session
		dictionary_list = search_mix(tags_query,gemList_query)
		# sorts dictionary in terms of gem value
		sorted_dictionary_list = sorted(dictionary_list, key = operator.itemgetter('likes_count'), reverse = True)
	return render_template('index.html', dictionary_list = sorted_dictionary_list, session = session)

def search_mix(tags_query,gemList_query): 
	dictionary_list = []
	if tags_query and gemList_query:
		api_url = 'https://8tracks.com/sets/new.json?api_key='+api+'?api_version=3'
		#mix_url = "http://8tracks.com/mix_sets/all.json?include=mixes[likes_count+3]&api_key="+api	
		top_tag_url = "http://8tracks.com/tags.json?api_key="+api
		# 8tracks API only accepts space as underscores 
		tags_query = tags_query.lower().replace(" ","_")
		
		for i in range(1,10):
			mix_url = "http://8tracks.com/mix_sets/tags:"+tags_query+\
						":popular.json?include=mixes[likes_count]&page="+str(i)+\
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
						mix_dictionary = {}
						mix_dictionary['image'] = results['cover_urls']['sq133']
						mix_dictionary['path'] = results['path']
						
						mix_dictionary['likes_count'] = results['likes_count']
						mix_dictionary['certification'] = results['certification']
						mix_dictionary['name'] = results['name']

						
						dictionary_list.append(mix_dictionary)
	return dictionary_list

if __name__ == '__main__':
	app.debug = True
	app.run()
