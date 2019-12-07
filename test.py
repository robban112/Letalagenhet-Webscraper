from WebScraper import scrapePages 
from _HTMLParser import *


#This is a test file :)

applist = getPageContent(SOLLENTUNA_HEM)
applist = filter(lambda x: x != None, applist)
applist = map(lambda x: x.getJSON(), applist)
print(list(applist))