import urllib2
url = 'http://www.baer-service.de/ergebnisliste.php?lid=GAU&jahr=2015&sort=`strecke`,`geschlecht`,`platzTotal`,`bruttozeit`&geschlecht=&page=0'

def search_pages(leading_url):
	print leading_url
	#get last character
	trailingchar = leading_url[-1:]
	#turn into int
	trailingnumber = int(trailingchar)

	#line wihtout last char
	input_line = leading_url[:-1]

	#increment trailingchar
	trailingnumber = trailingnumber + 1

	#append to input_line
	new_url = input_line + str(trailingnumber)
	print new_url

search_pages(url)