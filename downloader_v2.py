from bs4 import BeautifulSoup
import importlib, requests, urllib, os, time, sys, re, math


class app():

    def __init__(self):
        self.hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.42 Safari/537.36 Edg/77.0.235.17"}
        self.filters = {'http://www.directorylister.com', 'None', '..', 'javascript:void(0)', '[To Parent Directory]', '/cdn-cgi/l/email-protection', '/', 'aspnet_client'}
        self.files = {'jpg', 'jpeg', 'png', 'flac', 'mkv', 'exe', 'f4v', 'mp4', 'wmv', 'txt', 'iso', 'zip', 'rar', 'bmp', 'pdf'}
        self.site = 'http://misc.wirbelwind.ws/'
        self.root = os.getcwd()
        self.main()

    #NOTES
    #loops with folder in folder

    def filter(self, name, ext):
        if (ext in self.filters): pass
        elif name.lower() == ext and name not in self.filters: self.main(ext)
        elif (ext in self.files): self.getFiles(name, ext)
        return

    def checkPath(self, path):
        if os.path.exists(self.root + path): return (self.root + path)
        elif not os.path.exists(self.root + path):
            try: 
                child = (os.getcwd() + '\\' + path).replace('/', '\\').replace('\\\\', '\\')
                os.mkdir(child)
            except:
                pass

        return str(child)

    def getFolder(self, site, soup):
        links = soup.find_all('a')
        if len(links[0].get('href')) > 1: links.pop(0)
        for j in links:
            parsed = str(j.get('href')).split('.')
            if len(parsed) == 1: name = parsed[0]
            else: name = '.'.join(parsed[:-1])
            ext = parsed[-1].lower()
            self.filter(name, ext)
        return

    def getFiles(self, name, ext):
        print(f"\nCurrent directory is: {os.getcwd()}")

        fi = name + '.' + ext
        if not os.path.exists(self.root + fi):
            with open(self.root + fi, 'wb') as f: #DOWNLOADS FILE
                print (f"\nDownloading {name}.{ext}")
                response = requests.get(self.site + fi, stream = True)
                total_length = response.headers.get('content-length')

                if total_length is None:
                    f.write(response.content)

                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size = int(math.ceil(total_length / 100))):
                        dl += len(data)
                        f.write(data)
                        done = int(25 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('~' * done, ' ' * (25-done)))    
                        sys.stdout.flush()
        else:
            print((f"\nSkipping {name}.{ext}"))

    def main(self, ext = ""):
        if ext:
            os.chdir(self.root)
            print(f"\nTraversing into {ext}.")
            os.chdir(self.checkPath(ext))

        req = requests.get(self.site + ext, headers = self.hdr)
        soup = BeautifulSoup(req.text, 'html.parser')
        self.getFolder(self.site + ext, soup)
        return

if __name__ == "__main__":
    app()
#this section above can be modified to find different elements from different websites
