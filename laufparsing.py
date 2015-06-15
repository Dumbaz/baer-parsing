from bs4 import BeautifulSoup
import io
import csv
import datetime

now = datetime.datetime.now()

# -*- coding: iso-8859-1 -*-

soup = BeautifulSoup(open("Ergebnisliste.xls"), from_encoding="utf-8")

laufnameraw = soup.find('row').get_text()
laufname = "".join(laufnameraw)


print laufname.encode('utf-8')

localFile = open("%d_" % now.day + "%d_" %now.month + "%d_" %now.year + "%d_" %now.hour + "%d_" %now.minute + "%d" %now.second + '.csv' , 'wb')



def get_elements(soup):
	for row_tag in soup.findAll('row'):
		csvelement = row_tag.get_text("|").encode('utf-8'), row_tag.next_sibling
		if len(str(csvelement)) > 20:
			s = str(csvelement[0])
			u = unicode(s, "utf-8")
			strippedele = "".join(u.split("\n"))
			trailingnewline = strippedele + "\n"
			localFile.write(trailingnewline[1:].encode('utf-8'))
			print trailingnewline.encode('utf-8')


get_elements(soup)

localFile.close()

#def test_file(filename):
	# do all the checks
		#count elements in second row
		#compare ammount to all the other rows
	#print "there are errors"
	#print "Everything is a-OK"

	