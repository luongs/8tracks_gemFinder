8tracks_gemFinder
=================

The 8tracks gem finder interacts with 8tracks' API in order to pull gem certified 
mixes. Written in python using the Flask framework.  

================
Next steps:
* How to display mix pictures?
* Improve UI 
	* Better table
		* Have entries side by side 
		* Max 5 entries/row
	* Sort table as pictures
	* Limit number of entries/page
		* Therefore have automatic pagination

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

================
To consider: 
* Minor Bug: adding spaces disables session save
* Create better secret key

================
Future features: 
* Find certified mixes for a user's profile (eg: find all gold mixes published by a user)
* Play mixes from the website
	* Enable forwarding
* Log in to your account and add mixes directly
* AJAX autocomplete for input boxes
