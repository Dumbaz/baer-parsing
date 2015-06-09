from bs4 import BeautifulSoup
import io
import csv

soup = BeautifulSoup(open("Ergebnisliste.xls"), from_encoding="utf-8")

text = soup.get_text()

# print ( text.encode('utf-8') )

rows = soup.findAll('row')

output = io.BytesIO()
writer = csv.writer(output)

for row in rows:
	if len(row.text) > 1:
		writer.writerow( row.text.encode('utf-8') )
	print output.getvalue()

#writer.writerow(rows.text)
#output.getvalue()


#i = 0
#for row in rows:
#	if len(row.text) > 1:
#		print 'Row %s' %i
#		print row.text.encode('utf-8')
#		i = i+1

# print soup.prettify().encode('utf-8')