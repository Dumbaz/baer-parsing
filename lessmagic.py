from bs4 import BeautifulSoup

# ask for a file

# create the soup object
soup = BeautifulSoup(open("Ergebnisliste.xls"))

# Go for the table
table = soup.find("table")

print table