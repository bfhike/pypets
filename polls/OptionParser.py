from HTMLParser import HTMLParser


class OptionParser(HTMLParser):
    URL_FORMAT = 'https://www.google.com/search?q=pets+images+{0}&num=5&tbm=isch&tbo=u&source=univ&sa=X&bih=648'
    IMAGE_URL_ATTR_START = "imgurl="
    IMAGE_URL_ATTR_END = "&amp;"
    HREF_ATTR = "href"
    urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == self.HREF_ATTR:
                    start = attr[1].find(self.IMAGE_URL_ATTR_START)
                    if start > -1:
                        end = attr[1].find(self.IMAGE_URL_ATTR_END)
                        self.urls.append(attr[1][start:end])
                        break

    @staticmethod
    def search(term):
        connection = urllib.urlopen(self.URL_FORMAT.format(term))
        connection.read()

# instantiate the parser and fed it some HTML
# main = OptionParser()
# main.search('dog')
# main.urls
