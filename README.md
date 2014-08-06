8tracks_gemFinder
=================

The 8tracks gem finder interacts with 8tracks' API in order to pull gem certified 
mixes. Written in python using the Flask framework.  

================ 
Progress: 

* The 8tracks API is successfully queried for mixes and prints out the top 10 return queries
  for specific mix types
* Filtering queries in order to return specific certifications [gem/gold/platinum]
* Returns queries for the top 10 pages in trending or popular
* Allow user input for different tags and certifications	
* Implement form to allow user input and search for tags

================
Next steps:
* Sort results if more than 1 certification is selected
* Display return queries on webpage 
* Improve UI 


================
Future features: 
* Find certified mixes for a user's profile (eg: find all gold mixes published by a user)
* Play mixes from the website
	* Enable forwarding
* Log in to your account and add mixes directly
