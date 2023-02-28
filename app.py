import requests
import json
from bs4 import BeautifulSoup as BSoup
import os
from datetime import datetime
from tqdm.contrib.concurrent import thread_map
import re

def getnum():
    try:
        global num
        num=int(input("Number of wallpapers: "))
    except:
        print("Invalid value!")
        getnum()

def saveimg(url):
    if "png" in url:
        with open(f'{image_links[url]}.png',"wb") as f:
            f.write(s.get(url,stream=True).content)
    else:
        with open(f'{image_links[url]}.jpg',"wb") as f:
            f.write(s.get(url,stream=True).content)
    
def check(link,title):
    name=(title+" "+str(datetime.today().strftime('%Y %m %d %H %M %S')))
    if "png" in link:
        if len(image_links)!=num and link not in image_links:
            print("Wallpaper title: ",title," => Format: png!")
            image_links[link]=name
    elif "jpg" in link:
        if len(image_links)!=num and link not in image_links:
            print("Wallpaper title: ",title," => Format: jpg!")
            image_links[link]=name
    elif "gallery" in link:
        soup=BSoup(s.get(link,headers=headers).content, 'html.parser')
        images=soup.find_all('a', class_="_3BxRNDoASi9FbGX01ewiLg iUP9nbvcaxfwKrQTgt0sw")
        print(f'Wallpaper title: "{title}" => Format: gallery (with {len(images)} images)!')
        for index,image in enumerate(images):
            if len(image_links)!=num and link not in image_links:
                pic = image['href']
                image_links[pic]=name+" "+str(index)

def main():
    wall=json.loads(s.get("https://www.reddit.com/r/wallpaper/random/.json",headers=headers).text)[0]
    url=wall["data"]["children"][0]["data"]["url"]
    title=re.sub(r'[^\w\s]','',wall["data"]["children"][0]["data"]["title"])
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
    path=('Images '+str(datetime.today().strftime('%Y %m %d %H %M %S')))
    try:
        os.mkdir(os.path.join(os.getcwd(), path))
        os.chdir(os.path.join(os.getcwd(), path))
    except:
        pass
    getnum()
    while True:
        if len(image_links)==num:
            print(f'Saving {len(image_links)} wallpapers!')
            break
        else:
            main()
    thread_map(saveimg,image_links,max_workers=len(image_links))
        
