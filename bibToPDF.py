import pdfkit
import re
import urllib2
import os

from urlparse import urlparse

# Open the file
with open ("ref_liste.bib", "r") as myfile:
    data=myfile.read()#.replace('\n', '')

# Create the list
listOrig = re.findall("url = {.+}", data)
listStripped = []

# Strip the url = { and } and store in listStripped
for l in listOrig:
    listStripped.append(l[7:-1])

options = {
    'quiet' : '',
    'load-error-handling' : 'ignore'
}

for l in listStripped:
    print l
    url = urlparse(l)
    
    path = url.path[1:].split("/")

    tmp = url.netloc
    for i in range(0, len(path)-1):
        tmp += "/"+path[i]

    if not os.path.exists(tmp):
        os.makedirs(tmp)  

    name = path[len(path)-1]
    if name == "":
        name = "index"

    if not ".pdf" in l:
        # Strip bad chars
        print "\tprint to "+name
        try:
            pdfkit.from_url(l, tmp+"/"+name+".pdf", options=options)
        except:
            print "The following didn't work: "+l
        print "\tCompleted"
    else:
        print "\tpdf, saving.."
        response = urllib2.urlopen(l)
        file = open(tmp+"/"+name+".pdf", 'w')
        file.write(response.read())
        file.close()
        print "\tCompleted"

