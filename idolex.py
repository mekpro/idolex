import requests
import sqlite3
from bs4 import BeautifulSoup

DOWNLOAD_DIR = "/home/media/mekpro/Storage/pb/idolex"
WEB = "http://www.idolex.com"
START_INDEX = 1
END_INDEX = 2

def init_db():
    conn = sqlite3.connect('idolex.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS jobs')
    c.execute('''CREATE TABLE jobs
              (pageurl text unique, downloadurl text, loaded integer)''')
    conn.commit()
    conn.close()

def insert_job(page_url, download_url):
    conn = sqlite3.connect('idolex.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO jobs VALUES("%s","%s", "%d")' %(page_url, download_url, 0))
    conn.commit()
    conn.close()

def show_db():
    conn = sqlite3.connect('idolex.db')
    c = conn.cursor()
    for row in c.execute('select * from jobs'):
        print row

def get_pagelist(index_page):
    soup = BeautifulSoup(index_page)
    pagelist = []
    for page_link in soup.findAll("h2", { "class" : "title"}):
        pagelist.append(page_link.a["href"])
    return pagelist

def get_imagedownloadurl(photo_page):
    soup = BeautifulSoup(photo_page)
    download_a = soup.select('a[href^="http://ul.to"]')[0]
    download_url = download_a["href"]
    return download_url

def create_jobs():
    for page_id in range(START_INDEX, END_INDEX):
        r = requests.get(WEB + '/page/' + str(page_id))
        index_page = r.text
        pageurl_list = get_pagelist(index_page)
        for pageurl in pageurl_list:
            r = requests.get(pageurl)
            photo_page = r.text
            download_url = get_imagedownloadurl(photo_page)
            insert_job(pageurl, download_url)

def download_jobs():
    conn = sqlite3.connect('idolex.db')
    c = conn.cursor()


if __name__ == '__main__':
    #init_db()
    create_jobs()
    show_db()

