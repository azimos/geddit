#!/usr/bin/python
import requests
import json
# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
user_title = form.getvalue('search_title')




print "Content-type: text/html\n\n";

# Setting attributes to send to Wikipedia API
baseurl = 'http://en.wikipedia.org/w/api.php'

search_atts = {}
search_atts['action'] = 'query'
search_atts['list'] = 'search' 
search_atts['srwhat'] = 'text'
search_atts['format'] = 'json'   
search_atts['srsearch'] = user_title

search_resp = requests.get(baseurl, params = search_atts)

search_data = search_resp.json()


title = search_data["query"]["search"][0]["title"]

# Make the title with no space which will be needed for making a url link to send for summary
title_w_no_space = ""
for i in title:
	if i==" ":
		title_w_no_space = title_w_no_space + "_"
	else:
		title_w_no_space = title_w_no_space + i


 # Getting related topics using the result given by Wikipedia API
topics = []
for key in search_data["query"]["search"]:
	topics.append (key["title"])

topics =  topics [1:len(topics)]


# Summarizing the content:
# setting attributes for to send to Smmry API

link_for_smmry = 'https://en.wikipedia.org/wiki/' + title_w_no_space


smmry_base_url = 'http://api.smmry.com/'
#smmry_atts = {}
#smmry_atts ['SM_URL'] = 'https://en.wikipedia.org/wiki/Guyana'
#smmry_atts ['SM_API_KEY'] = '6F297A53E3'	       # represents your registered API key.
# Optional, X represents the webpage to summarize.
#smmry_atts ['SM_LENGTH'] = N        # Optional, N represents the number of sentences returned, default is 7 
#smmry_atts ['SM_KEYWORD_COUNT'] = N # Optional, N represents how many of the top keywords to return
#smmry_atts ['SM_QUOTE_AVOID']     # Optional, summary will not include quotations
#smmry_atts ['SM_WITH_BREAK']      # Optional, summary will contain string [BREAK] between each sentence
api_key_link = '&SM_API_KEY=6F297A53E3&SM_URL='
api_lenght = 'SM_LENGTH=7&SM_WITH_BREAK'
#print api_key_link
api_link = smmry_base_url + api_lenght + api_key_link + link_for_smmry

#smmry_resp = requests.get('http://api.smmry.com/&SM_API_KEY=6F297A53E3&SM_URL=https://en.wikipedia.org/wiki/Guyana')
smmry_resp = requests.get(api_link)

smmry_data = smmry_resp.json()

content= '<p>Try adding another key word.</p><a style="color:white;" id="backbtn" href="#"  onclick="myFunction()" >Go back.</a>'

try:
	content = smmry_data['sm_api_content']
except:
	pass

content_with_non_ascii = ""

for word in content:
	if ord(word) < 128:
		content_with_non_ascii+=word
	else:
		content_with_non_ascii+= "?"

if len(content_with_non_ascii) >0:
	content = content_with_non_ascii


# replacing "[BREAK]"s with a new line
while "[BREAK]" in content:
	length = len (content)
	break_position = content.find("[BREAK]")
	content = content [0:break_position] + "<br><br>" + content [break_position+7: length]


print '<div id="all-cont-alt"><div class="select-nav"><div id="nav-top-main"><a id="backbtn" href="#"  onclick="myFunction()" ><i style=" position: relative;margin-left: 25px;background-color: #00cfb9;padding: 13px;top: 74px;border-radius: 16px;color: #ffffff;text-align: left;" class= "fa fa-chevron-left fa-2x"></i></a><h1>Geddit</h1></div></div>'
print '<div id="loaddddd"></div><div id="contentss">'
print '<h1 id="user-title">'
print user_title
print "</h1>"
print content
print '</div></div>'
print '<h3 class="related">Related Topics</h3>'
print '<div id="rel-holder">'
for key in topics:
	if all(ord(c) < 128 for c in key):
		print '<h5 class="related-topics" onclick="relatedFunction();">'
		print key
		print '</h5>'	
	else:
		pass
print '</div>'
