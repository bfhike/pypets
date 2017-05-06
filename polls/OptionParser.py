from html.parser import HTMLParser
from http.client import HTTPSConnection

class OptionParser(HTMLParser):

    URL_HOST = 'www.google.com'
    URL_FORMAT = '/search?q=pets+images+{0}&num=5&tbm=isch&tbo=u&source=univ&sa=X&bih=648'
    IMAGE_URL_ATTR_START = "imgurl="
    IMAGE_URL_ATTR_END = "&amp;"
    HREF_ATTR = "href"
    urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == self.HREF_ATTR:
                    print(attr[1])
                    start = attr[1].find(self.IMAGE_URL_ATTR_START)
                    if start > -1:
                        end = attr[1].find(self.IMAGE_URL_ATTR_END)
                        self.urls.append(attr[1][start:end])
                        if len(self.urls) == 3:
                            self.reset()
                        else:
                            break

    def get(self, term):
        connection = HTTPSConnection(self.URL_HOST)
        connection.request("GET", self.URL_FORMAT.format(term))
        response = connection.getresponse()
        self.feed(str(response.read()))
        return self.urls

# instantiate the parser and fed it some HTML
# main = OptionParser()
# urls = main.get('dog')
# main.urls
