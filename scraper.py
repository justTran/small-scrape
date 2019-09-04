from bs4 import BeautifulSoup
import requests, urllib, urllib2, os, time, sys

reload(sys)
sys.setdefaultencoding('utf8') #for japanese characters
hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.42 Safari/537.36 Edg/77.0.235.17"}
sites = []
shouldContinue = True

print 'Enter a name for the output file\n'
name = raw_input()
out = open(name + '.txt', 'w')

print '\nEnter some URLs (type "stop" to reading)\n'

while(shouldContinue):
    link = raw_input()

    if link == 'stop':
        shouldContinue = False
        break

    else:
        sites.append(link)

if not sites:
    pass

else:
    for i in range(0, len(sites)):
        out.write('\n' + "Part " + str(i + 1) + '\n')
        req = requests.get(sites[i], headers = hdr)
        soup = BeautifulSoup(req.text, 'html.parser')
        for i in soup.find_all('li'):
            if (str(i.get('data-name')) == "None" or str(i.get('data-name')) == ".."):
                pass

            else:
                out.write(str(i.get('data-name')).encode() + '\n')

        #this section above can be modified to find different elements from different websites


print 'text parsing complete'
out.close()

