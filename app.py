import requests
import json
from bs4 import BeautifulSoup as BSoup
import os
from datetime import datetime
from tqdm.contrib.concurrent import thread_map
import re
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

class WallpaperMain:
    def __init__(self):
        self.pick=0
        self.num=0

    def ChooseWall(self):
        try:
            pick=int(input("Wallpaper type:\n=>(1)Random wallpaper\n=>(2)Search wallpaper\n=>(3)Random animated wallpapers\n=>(4)Search animated wallpapers: "))
            if pick>=1 and pick<=4:
                self.pick=pick
                def getnum():
                    try:
                        num=int(input("Number of wallpapers: "))
                        if num>0:
                            self.num=num
                        else:
                            print("Invalid value!")
                            getnum()
                    except:
                        print("Invalid value!")
                        getnum() 
                getnum()
            else:
                print("Invalid value!")
                self.ChooseWall()
        except:
            print("Invalid value!")
            self.ChooseWall()
        return self.pick, self.num

def saveFile(url):
    date=datetime.today().strftime(' %Y %m %d %H %M %S')
    with s.get(url) as r, open(f'{image_links[url]}{date}{os.path.splitext(urlparse(url).path)[1]}',"wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

class animatedWallpaper:
    def __init__(self):
        self.url="https://moewalls.com/"

    def netpage(self):
        while len(image_links)!=num and videoUrl.find("a",class_="next page-numbers"):
            nextUrl=videoUrl.find("a",class_="next page-numbers")["href"]
            self.mp4wall(nextUrl)

    def mp4wall(self,url):
        global videoUrl
        videoUrl=BSoup(s.get(url,headers=headers).text, 'html.parser')
        tag=videoUrl.find_all("a", class_="g1-frame")
        for x in tag:
            if len(image_links)!=num:
                link=x["href"]
                mainvid=BSoup(s.get(link,headers=headers).text, 'html.parser')
                linkdown=mainvid.find("video", class_="video-js vjs-default-skin vjs-big-play-centered").find("source")["src"]
                name=re.sub(r'[^\w\s]','',f'{x["title"]} {mainvid.find("ul",class_="list-inline").find_all("a",rel="tag")[1].text}')
                image_links[linkdown]=name
                print(f'Wallpaper title: {name} => Format: {os.path.splitext(urlparse(linkdown).path)[1]}!')
            else:
                break

    def randomAni(self):
        categoryLink=["https://moewalls.com/page/1/"]
        categoryName=["Random"]
        soup=BSoup(s.get(self.url,headers=headers).text, 'html.parser')
        category=soup.find("ul", class_="g1-secondary-nav-menu g1-menu-v")
        categoryUrl=category.find_all("a")
        for i in categoryUrl:
            categoryLink.append(i["href"])
            categoryName.append(i.text)
        for index,title in enumerate(categoryName):
            print(f'({index+1}): {title}')
        def pickCategory():
            try:
                CategoryNum=int(input("Pick a category: "))
                if CategoryNum>=1 and CategoryNum<=len(categoryName):
                    print("Selected: ",categoryName[CategoryNum-1])
                    self.mp4wall(categoryLink[CategoryNum-1])
                    self.netpage()
                else:
                    print("Invalid value!")
                    pickCategory()
            except:
                print("Invalid value!")
                pickCategory()
        pickCategory()
    
    def searchAni(self):
        query=(input("Search: ")).strip()
        searchUrl=f'{self.url}?s={query}'
        soup=BSoup(s.get(searchUrl,headers=headers).text, 'html.parser')
        if soup.find("a", class_="g1-frame"):
            self.mp4wall(searchUrl)
            self.netpage()
        else:
            print("No results found!")
            self.searchAni()

class imageWallpaper:
    def __init__(self):
        self.url="https://www.reddit.com"

    def check(self,link,title):
        if "gallery" in link:
            soup=BSoup(s.get(link,headers=headers).text, 'html.parser')
            images=soup.find_all('a', class_="_3BxRNDoASi9FbGX01ewiLg iUP9nbvcaxfwKrQTgt0sw")
            for index,image in enumerate(images):
                pic = image['href']
                if ".gif" not in pic and len(image_links)!=num and pic not in image_links:
                    print(f'Wallpaper title: {title} =>Index:  {index+1} => Format: {os.path.splitext(urlparse(pic).path)[1]}!')
                    image_links[pic]=f'{title} {index+1}'
                else:
                    break
        elif ".gif" not in link and len(image_links)!=num and link not in image_links:
            print(f'Wallpaper title: {title} => Format: {os.path.splitext(urlparse(link).path)[1]}!')
            image_links[link]=title

    def randomWall(self):
        while len(image_links)!=num:
            wall=json.loads(s.get(f'{self.url}/r/wallpaper/random/.json',headers=headers).text)[0]
            randomurl=wall["data"]["children"][0]["data"]["url"]
            title=re.sub(r'[^\w\s]','',wall["data"]["children"][0]["data"]["title"])
            self.check(randomurl,title)

    def searchImg(self):
        query=(input("Search: ")).strip()
        searchurl=f'{self.url}/r/wallpaper/search.json?q={query}&restrict_sr=1&include_over_18=1&limit=5&t=all'
        search_query=s.get(searchurl,headers=headers).json()
        if search_query["data"]["children"]:
            def get_after(x):
                global sWall
                sWall=s.get(x,headers=headers).json()
                length=sWall["data"]["children"]
                for x in range(len(length)):
                    if len(image_links)!=num and sWall["data"]["after"]:
                        link=sWall["data"]["children"][x]["data"]["url"]
                        title=re.sub(r'[^\w\s]','',sWall["data"]["children"][x]["data"]["title"])
                        self.check(link,title)
                    else:
                        break
            get_after(searchurl)
            while len(image_links)!=num and sWall["data"]["after"]:
                u = urlparse(searchurl)
                query = parse_qs(u.query, keep_blank_values=True)
                query.pop('after', None)
                u = u._replace(query=urlencode(query, True))
                urlafter=urlunparse(u)
                modurl=f'{urlafter}&after={sWall["data"]["after"]}'
                get_after(modurl)
        else:
            print("No results found!")
            self.searchImg()

if __name__=="__main__":
    print('''\033[96m
.-.-.-..---..-.   .-.   .---..---..---..---..---.  .--. .----..-.-.-..-..-..-.   .----..---..--. .---..---. 
| | | || | || |__ | |__ | |-'| | || |-'| |- | |-<  | \ \| || || | | || .` || |__ | || || | || \ \| |- | |-< 
`-----'`-^-'`----'`----'`-'  `-^-'`-'  `---'`-'`-' `-'-'`----'`-----'`-'`-'`----'`----'`-^-'`-'-'`---'`-'`-'
                                                                                By Jake10131               
    ''')
    s=requests.Session()
    headers = {
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    image_links={}
    path='wallpapers'+" "+str(datetime.today().strftime('%Y %m %d %H %M %S'))
    pick, num=WallpaperMain().ChooseWall()
    if pick:
        try:
            os.mkdir(os.path.join(os.getcwd(), path))
            os.chdir(os.path.join(os.getcwd(), path))
        except:
            pass

    if pick==1:
        imageWallpaper().randomWall()
    elif pick==2:
        imageWallpaper().searchImg()
    elif pick==4:
        animatedWallpaper().searchAni()
    else:
        animatedWallpaper().randomAni()
    print(f'Saving: {len(image_links)} wallpapers!')
    thread_map(saveFile,image_links,max_workers=os.cpu_count())
