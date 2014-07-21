from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json, pprint, urllib2

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DEBUG = True,
	SECRET_KEY = 'DevKey'
))

@app.route('/', methods=['GET','POST'])
def show_index():
	result = None
	api = 'API_KEY'
	api_url = 'https://8tracks.com/sets/new.json?api_key='+api+'?api_version=3'
	#mix_url = "http://8tracks.com/mix_sets/all.json?include=mixes[likes_count+3]&api_key="+api
	# How do you only show certain mixes passing the include qualifications??
	mix_url = "http://8tracks.com/mix_sets/tags:chill+weed.json?include=mixes[certification[gold]]&api_key="+api+'&api_version=3'
	top_tag_url = "http://8tracks.com/tags.json?api_key="+api	
	# genre = raw_input("Enter mood, genre or activity")
	r = requests.get(mix_url)
	r.text
	json_result = json.loads(r.text)
	#print(r.text)
	for results in json_result['mix_set']['mixes']:
		print "Mix name: "+results['name']
		print "Likes count: "+str(results['likes_count'])
		
	#for results in json_result['mixes']:
	#	print "Mix name: "+results['name']
	'''
	for results in json_result['tags']: 
		print "Tag name: " + results['name']
		print "Cool tagging count: "+ results['cool_taggings_count']
		print "------------------"	
	'''
	if request.method == 'POST':
		# get input request
		result = request.form['queryBox']
		# update result in html page
		flash(result)
	return render_template('index.html', result = result)

if __name__ == '__main__':
	app.debug = True
	app.run()