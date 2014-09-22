8tracks_gemFinder
=================

The 8tracks gem finder interacts with 8tracks' API in order to pull gem certified 
mixes. Written in python using the Flask framework.  

================
Next steps:

* Add arrow to 'Dig up popular mixes'
* Create an icon 
* Limit on an individual IP's search to prevent DoS

================ 
Completed: 

* The 8tracks API is successfully queried for mixes and prints out the top 10 return queries
  for specific mix types
* Filtering queries in order to return specific certifications [gem/gold/platinum]
* Returns queries for the top 10 pages in trending or popular
* Allow user input for different tags and certifications	
* Implement form to allow user input and search for tags
* Display return queries on webpage
* Dictionary must display all values instead of just one
* Sessions have been enabled for query input text and check boxes
* Optimize code (testing yielded similar results between n^3 and n^2 loops since n is still small)
* Sort results by gem level if more than 1 certification is selected 
* Display mix pictures 
* App is deployed on Heroku
* Create a secure and random secret key
* Remove secret key and api key from github commited file
* Update UI for mobile
* Incorporate link inside img src
* Add notice that no result has been found if results are empty

================
Future features: 
* Find certified mixes for a user's profile (eg: find all gold mixes published by a user)
* Play mixes from the website
	* Enable forwarding
* Randomize search button
* Log in to your account and add mixes directly
* AJAX autocomplete for input boxes
