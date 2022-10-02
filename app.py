import requests
from bs4 import BeautifulSoup as BSoup
import os
import datetime

def hd_image(no, path):
 try:
  os.mkdir(os.path.join(os.getcwd(), path))
 except:
  pass
 os.chdir(os.path.join(os.getcwd(), path))
 pageNo = 1
 while (pageNo <= no):
  url = f'https://wall.alphacoders.com/featured.php?page={str(pageNo)}'

  headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

  web = requests.get(url, headers=headers)

  soup = BSoup(web.content, 'html.parser')

  images = soup.find_all('img', class_="img-responsive")
  
  for image in images:
    link = image['src']
    name = image['alt']
    iname = name.replace("|", "")
    img_name = iname.replace(" ", "_")
    with open(str(img_name) + '.png', 'wb') as f:
            HdImg = requests.get(link)
            f.write(HdImg.content)
            print(f"Saving:{iname} PageNo:{pageNo}")
  pageNo += 1
            
no_pages = int(input("Numbers of pages to scrape:\n"))
time = datetime.datetime.now()
folder = ('Images-'+str(time))
hd_image(no_pages, folder)
