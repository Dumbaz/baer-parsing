import urllib2
url = 'http://www.baer-service.de/ergebnisliste.php?lid=GAU&jahr=2015&sort=`strecke`,`geschlecht`,`platzTotal`,`bruttozeit`&geschlecht=&page=0'

def search_pages(leading_url):
	print url
	#get last character
	trailingchar = leading_url[-1:]
	print trailingchar
	#turn into int
	trailingnumber = int(trailingchar)
	print trailingnumber

	#line wihtout last char
	input_line = leading_url[:-1]
	print input_line

	#increment trailingchar
	trailingnumber = trailingnumber + 1
	print trailingnumber

	#append to input_line
	new_url = input_line + str(trailingnumber)
	print new_url

search_pages(url)