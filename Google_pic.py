# -*- coding:utf-8 -*-
import mimetypes
import urllib
import urllib2

import time
from bs4 import BeautifulSoup
from urllib2 import urlopen
import os
import argparse
import json
from hashlib import sha1
import Queue
from threading import Thread

WORKER_THREADS = 40

q = Queue.Queue()
# Worker thread - retrieve from Queue and process data for downloading
def worker():
    while True:
        resData = q.get()
        if resData is None:
            print "resData is worry"
            break
        link = resData[0]
        Type = resData[1]
        DIR = resData[2]
        print "into downloading"
        print DIR
        try:
            link_header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
            }
            res = urlopen(urllib2.Request(link, headers=link_header))
            raw_img = res.read()
            filename = str(sha1(link.encode()).hexdigest()) + "." + Type
            print filename
            # sha1是使用哈希算法进行加密，生成160bit的结果，通常是使用40位的16进制数来保存，hexdigest()是生成16进制的md5加密结果
            if len(Type) != 0 and res.info().get("Content-Type") != "text/html":
                print res.info().get("Content-Type")
                print mimetypes.guess_type(filename)
                f = open(os.path.join(DIR, filename), 'wb')
                f.write(raw_img)
                f.close()
        except Exception as e:
            print("could not load : " + link)
            print(e)
        q.task_done()
        time.sleep(2)


def get_soup(url, header):
    url_content = urlopen(urllib2.Request(url, headers=header))
    if url_content:
        print "url_content"
        # print url_content
    print "you are beautiful"
    return BeautifulSoup(url_content, 'html.parser')


if __name__ == "__main__":
    """parser = argparse.ArgumentParser(
        description="Let's grab some pictures from Google")
    parser.add_argument('query', metavar='S', type=str,
                        help='the desired search query')
    args = parser.parse_args()
    query = args.query
    query = query.split(' ')
    query = '+'.join(query)
    print query
    print type(query)"""

    ret = []
    with open("label.txt", "r") as fin:
        for line in fin.readlines():
            spt = line.split(',')
            ret.append(spt[0])
    for query in ret:
        print query
        url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
        print url
        # add the directory for your image here
        DIR = "Pictures"
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = get_soup(url, header)
        time.sleep(2)
        print soup
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        DIR = os.path.join(DIR, query.split()[0])
        if not os.path.exists(DIR):
            os.mkdir(DIR)

        # Create Worker Threads
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            print link, Type
            q.put([link, Type, DIR])
        for i in range(WORKER_THREADS):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        q.join()
        time.sleep(8)
