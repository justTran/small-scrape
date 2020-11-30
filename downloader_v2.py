from bs4 import BeautifulSoup
import importlib, requests, urllib, os, time, sys, re

hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.42 Safari/537.36 Edg/77.0.235.17"}
filters = {'http://www.directorylister.com', 'None', '..', 'javascript:void(0)', '[To Parent Directory]', '/cdn-cgi/l/email-protection', '/'}
files = {'jpg', 'jpeg', 'png', 'flac', 'mkv', 'exe', 'f4v', 'mp4', 'wmv', 'txt', 'iso', 'zip', 'rar', 'bmp'}
badfiles = {'.url', '.nfo'}
site = 'http://misc.wirbelwind.ws/'
root = os.getcwd()

def filter(name, ext):
    if (ext in filters): pass
    elif name == ext and name not in filters: main(ext)
    elif (ext in badfiles): pass
    elif (ext in files): getFiles(name, ext)
    return

def checkPath(path):
    if os.path.exists(root + path): return (root + path)
    elif not os.path.exists(root + path):
        try: 
            child = (os.getcwd() + '\\' + path).replace('/', "")
            os.mkdir(child)
        except:
            pass

    return str(child)

def getFolder(site, soup):
    for j in soup.find_all('a'):
        parsed = str(j.get('href')).split('.')
        name = ''.join(parsed[:1])
        ext = parsed[-1].lower()
        filter(name, ext)
    return

def getFiles(name, ext):
    print(f"/nCurrent directory is: {os.getcwd()}")
    fi = name + '.' + ext
    with open(root + fi, 'wb') as f: #DOWNLOADS FILE
        print (f"\nDownloading {name}.{ext}")
        response = requests.get(site + fi, stream = True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)

        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size = int(total_length / 100)):
                dl += len(data)
                f.write(data)
                done = int(25 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('~' * done, ' ' * (25-done)))    
                sys.stdout.flush()

def main(ext = ""):
    if ext: 
        os.chdir(root)
        print(f"Traversing into {ext}.")
        os.chdir(checkPath(ext))

    req = requests.get(site + ext, headers = hdr)
    soup = BeautifulSoup(req.text, 'html.parser')
    getFolder(site + ext, soup)
    return

if __name__ == "__main__":
    main()
#this section above can be modified to find different elements from different websites
