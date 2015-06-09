from bs4 import BeautifulSoup
import io
import csv

soup = BeautifulSoup(open("Ergebnisliste.xls"), from_encoding="utf-8")

for row_tag in soup.findAll('row'):
	csvelement = row_tag.get_text("|").encode('utf-8'), row_tag.next_sibling
	if len(str(csvelement)) > 20:
		s = str(csvelement[0])
		u = unicode(s, "utf-8")
		strippedele = "".join(u.split("\n"))
		print strippedele.encode('utf-8')