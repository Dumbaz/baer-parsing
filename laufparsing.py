from bs4 import BeautifulSoup

soup = BeautifulSoup(open("Ergebnisliste.xls"), from_encoding="utf-8")

text = soup.get_text()

print ( text.encode('utf-8') )