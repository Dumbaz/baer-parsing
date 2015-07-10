from bs4 import BeautifulSoup
from datetime import date
import urllib2, random, csv

url_no_year = "http://www.baer-service.de/history.php?jahr="

# year for the first page
first_page_url = 2012

#first entries are from 1978
#get current year so we know where to end the loop
current_year = date.today().year

start = url_no_year + str(first_page_url)
end = url_no_year + str(current_year)

# save all URLs for a year of results
overview_url_list = []

#incrementing page URLs
def year_incrementer(year_variable):
	while year_variable <= current_year:
		urlstring = url_no_year + str(year_variable)
		#print urlstring
		overview_url_list.append(urlstring)
		year_variable = int(year_variable) + 1


year_incrementer(first_page_url)

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
random.seed()
user_agent = random.choice(user_agents)

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', user_agent)]

# Function to get the HTML
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

# Function to parse a contest
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

for url in overview_url_list:
	soup = BeautifulSoup(get_url(url))
	table = soup.find(lambda tag: tag.name=="table" and tag.has_attr('style') and tag['style']=="width:100%;")
	rows = table.findAll(lambda tag: tag.name=="tr")
	for row in rows:
		rowlength = row.findAll('a')
		if len(rowlength) == 2:
			contest_name = row.find(lambda tag: tag.name=="th").text.encode('utf-8')
			php_contest_url = row.find(lambda tag: tag.name=="a")
			full_url = "http://www.baer-service.de/" + php_contest_url['href'] + "&page=0"
			print full_url
			headers = []
			records = []
			parsing(full_url)
			with open(contest_name.replace(' ', '_').replace('.', '').replace('/', '-'), 'wb') as f:
				writer = csv.writer(f, delimiter='|')
				writer.writerows(headers)
				writer.writerows(records)

