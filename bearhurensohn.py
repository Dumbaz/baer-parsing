import urllib2
url = 'http://www.baer-service.de/ergebnisliste.php?lid=GAU&ak=&strecke=13,0%20km&sort=`geschlecht`,`platzTotal`&suche=&jahr=2015&style=&page=0'
anotherurl = 'http://dumbaz.de'

print len(urllib2.urlopen(url).read())

request = urllib2.Request(url, headers={'accept': '*/*'})

print len(urllib2.urlopen(request).read())