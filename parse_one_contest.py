from bs4 import BeautifulSoup
import urllib2
import os
import random
import datetime
import csv, codecs, cStringIO

# URL for the first page http://www.baer-service.de/ergebnisliste.php?lid=GAU&ak=&strecke=13,0%20km&sort=`geschlecht`,`platzTotal`&suche=&jahr=2015&style=&page=0
bearurl = "http://www.baer-service.de/ergebnisliste.php?lid=HZS&jahr=2015&sort=`strecke`,`geschlecht`,`platzTotal`,`bruttozeit`&geschlecht=" + "&page=0"

future_file_name = raw_input("Enter the name of the race \n").replace(' ', '_').replace('.', '')
print "File Name will be " + future_file_name + ".csv"
input_url = raw_input("Enter an URL \n")
print "Doing work...."

bearurl = input_url + "&page=0"

records = []
headers = []
        

# Global Variables etc
user_agents = [
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.45 Safari/534.13',
    'Opera/9.80 (X11; Linux i686; U; en) Presto/2.7.62 Version/11.00',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US))',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
    ]

connection_timeout = 90
# now = datetime.datetime.now()
# localFile = open("%d_" % now.day + "%d_" %now.month + "%d_" %now.year + "%d_" %now.hour + "%d_" %now.minute + "%d" %now.second + '.csv' , 'wb')

random.seed()
user_agent = random.choice(user_agents)

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', user_agent)]

# Get the HTML
def get_url(url, referer_url=None):
    '''Downloads specified URL and returns its contents. Returns false
    on fail.'''
    retries = 5
    while retries > 0:
        try:
            if referer_url:
                req = urllib2.Request(url, headers={'accept': '*/*'})
                req.add_header('Referer', referer_url)
                page = opener.open(req)
            else:
                page = opener.open(url, None, connection_timeout)
        except urllib2.URLError, e:
            if hasattr(e, 'code') and e.code == 503:
                return e.read()
            else:
                print('Download failed.')
                retries -= 1
                if retries > 0:
                    print('Retrying...')
        else:
            return page.read()
    print('Maximum number of retries reached.')
    return False


# Rewrites the url to hopefully change page=i to page=i+1
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
    return new_url

def parsing(url):
    soup = BeautifulSoup(get_url(url))
    # Cancel recursion
    if len(soup.findAll('td')) == 1:
        print 'Its over'
        return

    table = soup.find(lambda tag: tag.name=="table" and tag.has_attr('id') and tag['id']=="ergebnistabelle")
    table_headers = soup.findAll(lambda tag: tag.name=="th")
    if not headers:
        headers.append([elem.text.encode('utf-8').strip() for elem in table_headers])
    rows = table.findAll(lambda tag: tag.name=="tr")
    for tr in table.findAll('tr'):
        tds = tr.findAll('td')
        records.append([elem.text.encode('utf-8').lstrip() for elem in tds])
    parsing(search_pages(url))



parsing(bearurl)

with open(future_file_name, 'wb') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerows(headers)
    writer.writerows(records)