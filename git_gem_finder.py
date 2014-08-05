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
	# give choice to search through popular or trending		
	if request.method == 'POST':
		# get input request
		tags = request.form['queryBox']
		gemList = request.form.getlist('certification')
		search_mix(tags,gemList)
		# update result in html page
		flash(result)
	return render_template('index.html', result = result)

def search_mix(tags,gemList): 
	if tags and gemList:
		api = 'API_KEY'
		api_url = 'https://8tracks.com/sets/new.json?api_key='+api+'?api_version=3'
		#mix_url = "http://8tracks.com/mix_sets/all.json?include=mixes[likes_count+3]&api_key="+api	
		top_tag_url = "http://8tracks.com/tags.json?api_key="+api
		for i in range(1,10):
			mix_url = "http://8tracks.com/mix_sets/tags:"+tags+\
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
			#print(r.text)
			for results in json_result['mix_set']['mixes']:
				for gem in gemList:
					if (results['certification']==gem):
						print "Mix name: "+results['name']
						print "Likes count: "+str(results['likes_count'])
						print "Certification: "+results['certification']
						print "8tracks path: "+results['path']
						print "# requests left: "+r.headers['x-requests-left']
						print "Page found: "+str(i)

if __name__ == '__main__':
	app.debug = True
	app.run()