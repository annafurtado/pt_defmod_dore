# Gutenberg Project:  a collection of books. 
url = 'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm'

#####################  REQUESTS  #####################
import requests  ##HTTP library - more favorable, fewer lines of codes for authentication etc. 
# Make the request and check object type
r = requests.get(url)
#print(type(r))
#print(r.ok) # if it is a valid page, it will return True. 
#print(r.status_code) # 200 for a valid URL, 404 for a non-existing URL. 
#print(r.content)  # same as view page source - content in bytes, for especially non-text

# Extract HTML from Response object and print
html = r.text  # in Unicode
#print(html)


#####################  URLLIB  #####################
from urllib.request import urlopen  ##Standard Python library, it has parsing functionality as well, faster than requests. 
response = urlopen(url) # send the request
data = response.read() # read the content in the response package

#print(response.code)
#print(type(data))
#print(data)  # data in binary format. 

html = data.decode("UTF-8")
#print(type(html)) ## not in binary format anymore, decoded into UTF8. 
#print(html)

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html5lib") # define the BeautifulSoup object.
print(type(soup)) # a BeautifulSoup object.
print(soup.h1) # the first header in the source
print(soup.title) # the title specified in the html source
print(soup.title.string) # get rid of html tags
print(soup.find_all('a')[:8]) # find all hyperlinks in the source, print first 8 of them
print(len(soup.findAll('a'))) # how many hyperlinks are there in the web page? 

moby_dick_text= soup.get_text() #get rid of all html tags to extract the plain text. Use only if you need raw/plain text for your NLP task
print(moby_dick_text)


from urllib.request import urlopen
from bs4 import BeautifulSoup

response3 = urlopen("http://www.pythonscraping.com/pages/page3.html")
soup = BeautifulSoup(response3)
print(soup.prettify()) # it prints in a pretty format with all indentations in the page source

for child in soup.find("table", {"id":"giftList"}).children: # find the tables with id=giftList and visit all children in the table (i.e. rows of the table)
  print(child)

for desc in soup.find("table", {"id":"giftList"}).descendants: # find the tables with id=giftList and visit all descendants in the table 
  print(desc)

for sibling in soup.find("table", {"id":"giftList"}).tr.next_siblings: # find the tables with id=giftList, move to the first row, then visit the subsequent rows
  print(sibling)

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "http://www.pythonscraping.com/pages/page3.html"
response = urlopen(url)
soup = BeautifulSoup(response)
images = soup.findAll("img", {"src":re.compile("\.\.\/img\/gifts\/img.*\.[jpg|png|jpeg]")})  # ../img/gifts/img.jpg

for image in images:
  print(image["src"])


import re

sentence = "peter piper pick a peck of pickled peppers"

ps = 'p\w+'

print(re.findall(ps, sentence))
print(re.findall('\w+', sentence))
print(re.findall('\w+', moby_dick_text))

