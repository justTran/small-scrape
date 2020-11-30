from bs4 import BeautifulSoup
import requests, urllib, urllib2, os, time, sys

hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.42 Safari/537.36 Edg/77.0.235.17"}
filters = ['http://www.directorylister.com', 'None', '..', 'javascript:void(0)', 'https://archive.koba.li/', 'https://archive.koba.li/?dir=Music', 'https://archive.koba.li/?dir=Music%2FAnime%20Music', '/cdn-cgi/l/email-protection', 'https://archive.koba.li/?dir=Music%2FAnime%20Music%2FAnime%20OST%20Sammlung%20Part%201']
files = ['.jpg', '.JPG', 'jpeg', 'JPEG', '.png', '.PNG', 'flac', 'FLAC','.mkv', '.MKV', '.exe', '.EXE', '.f4v', '.F4V', '.mp4', '.MP4', '.wmv', '.WMV', '.txt', '.TXT', '.iso', '.ISO', '.zip', '.ZIP', '.rar', '.RAR', '.bmp', '.BMP', 'None']
badfiles = ['.url', '.nfo']
#site = 'https://archive.koba.li/?dir=Music/Anime%20Music/Anime%20OST%20Sammlung%20Part%201/%5BASL%5D%20765PRO%20ALLSTARS%20-%20THE%20IDOLM%40STER%20MOVIE%20Kagayaki%20no%20Mukougawa%20e%21%20Insert%20Song%20-%20Ramune-iro%20Seishun%20%5BFLAC%5D'
site = 'https://archive.koba.li/?dir=Music%2FAnime%20Music%2FAnime%20OST%20Sammlung%20Part%20'
root = os.getcwd()


def getFolder(site, soup):
    for j in soup.find_all('a'):
        os.chdir(root)
        if (str(j.get('href')) in filters):
            pass

        elif (str(j.get('href')) == site):
            pass

        elif (str(j.get('href'))[-4:] in files):
            pass

        elif (str(j.get('href'))[-4:] in badfiles):
            pass

        else:
            print("\nParent %s, we have: \n" % str(j.get('data-name')))
            if os.path.exists(str(j.get('data-name'))):
                pass
        
            elif not os.path.exists(str(j.get('data-name'))):
                try:
                    #print("making a new path")
                    parent = os.getcwd() + '//' + str(j.get('data-name'))
                    os.makedirs(parent)
                    os.chdir(parent)
                except:
                    pass
                r = requests.get('https://archive.koba.li/' + str(j.get('href')), headers = hdr)
                newSoup = BeautifulSoup(r.text, 'html.parser')
                for k in newSoup.find_all('a'):
                    os.chdir(parent)
                    if (str(k.get('href')) in filters):
                        pass

                    elif (str(k.get('href'))[-4:] in files):
                        #print(str(k.get('data-name')))
                        getFiles(k)

                    elif (str(k.get('href'))[-4:] in badfiles):
                        pass

                    else:
                        print("\nInside %s, we have: \n" % str(k.get('data-name')))
                        if not os.path.exists(str(k.get('data-name'))):
                            try:
                                #print("making a new path")
                                child = parent + '//' + str(k.get('data-name'))
                                os.makedirs(child)
                            except:
                                pass
                        newSite = "https://archive.koba.li/" + str(k.get('href'))
                        r2 = requests.get(newSite, headers = hdr)
                        childSoup = BeautifulSoup(r2.text, 'html.parser')
                        for l in childSoup.find_all('a'):
                            os.chdir(child)
                            if (str(l.get('href')) in filters):
                                pass

                            elif (str(l.get('href'))[-4:] in files):
                                #print(str(l.get('data-name')))
                                getFiles(l)

                            elif (str(l.get('href'))[-4:] in badfiles):
                                pass

def getFiles(file):
    name = str(file.get('data-name'))
    with open(name, 'wb') as f: #DOWNLOADS FILE
        print ("\nDownloading %s" % name)
        response = requests.get('https://archive.koba.li/' + str(file.get('href')), stream = True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)

        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size = total_length / 100):
                dl += len(data)
                f.write(data)
                done = int(25 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('~' * done, ' ' * (25-done)))    
                sys.stdout.flush()

def main():
    reload(sys)
    sys.setdefaultencoding('utf8') #for japanese characters
    for i in range(10, 11):
        try:
            req = requests.get(site + str(i), headers = hdr)
            soup = BeautifulSoup(req.text, 'html.parser')
            getFolder(site + str(i), soup)
        except:
            pass

if __name__ == "__main__":
    main()
#this section above can be modified to find different elements from different websites
