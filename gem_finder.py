from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json, operator, os, collections

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
	api = app.config['API_KEY']	# retrieve API key from local config file
else:
	api = os.environ.get('API_KEY')	# retrieve API key from heroku config vars
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')	# set SECRET_KEY from heroku

@app.route('/', methods=['GET','POST'])
def show_index():
	result = None
	dictionary_list = []
	sorted_dictionary_list = []
	gemList_query = []
	popular_tag_list = []
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
	else:
		popular_tag_list = get_popular_tags()
	return render_template('index.html', dictionary_list = sorted_dictionary_list, popular_tag_list = popular_tag_list, session = session)

@app.route("/sitemap.xml", methods=["GET"])
def sitemap():	
    return render_template('sitemap.xml')

def get_popular_tags():
	popular_tag_list = []
	top_tag_url = 'http://8tracks.com/tags.json?api_key='+api+'?api_version=3'
	r = requests.get(top_tag_url)
	r.text
	json_result = json.loads(r.text)
	for tag_cloud in json_result['tag_cloud']['tags']:
		popular_tag_list.append(tag_cloud['name'])
	return popular_tag_list 


def search_mix(tags_query,gemList_query): 
	dictionary_list = []
	if tags_query and gemList_query:
		MAX_PAGE = 10
		FILTER = "popular"
		# 8tracks API only accepts space as underscores 
		tags_query = tags_query.lower().replace(" ","_")
		
		# detect if 'gem' has been picked from list
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
						# use ordered dictionary to retrieve keys in the same order they were added 
						mix_dictionary = collections.OrderedDict()
						image_path =[results['path'], results['cover_urls']['sq133']]
						mix_dictionary['img_path'] = image_path		#list must be used to hold both items
						mix_dictionary['name'] = results['name']
						mix_dictionary['certification'] = results['certification']
						mix_dictionary['likes_count'] = results['likes_count']
						dictionary_list.append(mix_dictionary)
			# list is empty
	if not dictionary_list:
		mix_dictionary = collections.OrderedDict()
		mix_dictionary['name'] ='-'
		mix_dictionary['certification'] = '-'
		mix_dictionary['likes_count'] = 0
		mix_dictionary[''] = 'No mixes found! Try again with different tags or certifications'
		dictionary_list.append(mix_dictionary)
	return dictionary_list

if __name__ == '__main__':
	app.debug = True
	app.run()
