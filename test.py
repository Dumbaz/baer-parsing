def search_pages(leading_url):
    print leading_url
    #get the page number modificator
    pageNum = int(leading_url.split("page=")[len(leading_url.split("page="))-1])

    #line wihtout last char
    input_line = leading_url.split("page=")[0]

    #increment trailingchar
    pageNum = pageNum + 1

    #append to input_line
    new_url = input_line + "page=" + str(pageNum)
    print new_url
    return new_url


search_pages("http://www.baer-service.de/ergebnisliste.php?lid=GAU&ak=&strecke=13,0%20km&sort=`geschlecht`,`platzTotal`&suche=&jahr=2015&style=&page=9")