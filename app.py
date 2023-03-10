import requests
import json
from bs4 import BeautifulSoup as BSoup
import os
from datetime import datetime
from tqdm.contrib.concurrent import thread_map
import re
import shutil
from urllib.parse import urlparse

def ChooseWall():
    def getnum():
        try:
            global num
            num=int(input("Number of wallpapers: "))
            if num<=0:
                print("Invalid value!")
                getnum()
        except:
            print("Invalid value!")
            getnum() 

    try:
        global pick
        pick=int(input("Wallpaper type (1)png/jpg (2)mp4: "))
        if pick==1 or pick==2:
            getnum()
        else:
            print("Invalid value!")
            ChooseWall()
    except:
        print("Invalid value!")
        ChooseWall()

def saveFile(url):
    date=datetime.today().strftime(' %Y %m %d %H %M %S')
    with s.get(url, stream=True) as r, open(f'{image_links[url]}{date}{os.path.splitext(urlparse(url).path)[1]}',"wb") as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw,f,length=16384)

def liveWall():
    categoryLink=["https://moewalls.com/page/1/"]
    categoryName=["Random"]

    url="https://moewalls.com/"

    soup=BSoup(s.get(url,headers=headers).content, 'html.parser')

    category=soup.find("ul", class_="g1-secondary-nav-menu g1-menu-v")

    categoryUrl=category.find_all("a")

    for i in categoryUrl:
        categoryLink.append(i["href"])
        categoryName.append(i.text)

    for index,title in enumerate(categoryName):
        print(f'({index+1}): {title}')

    def mp4wall(url):
        global videoUrl
        videoUrl=BSoup(s.get(url,headers=headers).content, 'html.parser')
        tag=videoUrl.find_all("a", class_="g1-frame")
        for x in tag:
            if len(image_links)!=num:
                link=x["href"]
                mainvid=BSoup(s.get(link,headers=headers).content, 'html.parser')
                linkdown=mainvid.find("video", class_="video-js vjs-default-skin vjs-big-play-centered").find("source")["src"]
                name=re.sub(r'[^\w\s]','',f'{x["title"]} {mainvid.find("ul",class_="list-inline").find_all("a",rel="tag")[1].text}')
                image_links[linkdown]=name
                print(f'Wallpaper title: {name} => Format: {os.path.splitext(urlparse(linkdown).path)[1]}!')
            else:
                break

    def pickCategory():
        try:
            CategoryNum=int(input("Pick a category: "))
            if CategoryNum>=1 and CategoryNum<=len(categoryName):
                print("Selected: ",categoryName[CategoryNum-1])
                mp4wall(categoryLink[CategoryNum-1])
            else:
                print("Invalid value!")
                pickCategory()
        except:
            print("Invalid value!")
            pickCategory()
    pickCategory()
    while len(image_links)!=num and bool(videoUrl.find("a",class_="next page-numbers")):
        nextUrl=videoUrl.find("a",class_="next page-numbers")["href"]
        mp4wall(nextUrl)

def imagewall():
    wall=json.loads(s.get("https://www.reddit.com/r/wallpaper/random/.json",headers=headers).text)[0]
    url=wall["data"]["children"][0]["data"]["url"]
    title=re.sub(r'[^\w\s]','',wall["data"]["children"][0]["data"]["title"])

    def check(link,title):
        if ".png" in link or ".jpg" in link:
            if len(image_links)!=num and link not in image_links:
                print(f'Wallpaper title: {title} => Format: {os.path.splitext(urlparse(link).path)[1]}!')
                image_links[link]=title
        elif "gallery" in link:
            images=BSoup(s.get(link,headers=headers).content, 'html.parser').find_all('a', class_="_3BxRNDoASi9FbGX01ewiLg iUP9nbvcaxfwKrQTgt0sw")
            if link not in image_links: print(f'Wallpaper title: "{title}" => Format: gallery (with {len(images)} images)!')
            for index,image in enumerate(images):
                if len(image_links)!=num and link not in image_links:
                    pic = image['href']
                    image_links[pic]=f'{title} {index+1}'
    check(url,title)

if __name__=="__main__":
    print('''\033[96m
.-.-.-..---..-.   .-.   .---..---..---..---..---.  .--. .----..-.-.-..-..-..-.   .----..---..--. .---..---. 
| | | || | || |__ | |__ | |-'| | || |-'| |- | |-<  | \ \| || || | | || .` || |__ | || || | || \ \| |- | |-< 
`-----'`-^-'`----'`----'`-'  `-^-'`-'  `---'`-'`-' `-'-'`----'`-----'`-'`-'`----'`----'`-^-'`-'-'`---'`-'`-'
                                                                                By Jake10131               
    ''')
    s=requests.Session()
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36","Cache-Control": "no-cache", "Pragma": "no-cache"}
    image_links={}
    path='wallpapers'+" "+str(datetime.today().strftime('%Y %m %d %H %M %S'))
    try:
        os.mkdir(os.path.join(os.getcwd(), path))
        os.chdir(os.path.join(os.getcwd(), path))
    except:
        pass
    ChooseWall()
    if pick==1:
        while len(image_links)!=num:
            imagewall()
    elif pick==2:
        liveWall()
    print(f'Saving: {len(image_links)} wallpapers!')
    thread_map(saveFile,image_links,max_workers=len(image_links))
