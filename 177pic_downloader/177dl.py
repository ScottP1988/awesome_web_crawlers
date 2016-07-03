#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import bs4
import requests
import urllib2


def _get_content(url):
    return requests.get(url).content


def _url_parser(raw_url):
    return raw_url.split('.html')[0] + '.html'


def _get_page_list(url):
    content = _get_content(url)
    page_list = []
    page_list.append(url)
    soup = bs4.BeautifulSoup(content, 'html.parser')
    entry = soup.find('div', attrs={'class': 'wp-pagenavi'})
    for n in entry.find_all('span', attrs={'class': 'single-navi'}):
        if n.get_text() != '1':
            page_list.append(page_list[0] + '/' + n.get_text())
    return page_list


def _get_images_url(page_list):
    images = []
    for page in page_list:
        content = _get_content(page)
        soup = bs4.BeautifulSoup(content, 'html.parser')
        entry = soup.find('div', attrs={'class': 'entry-content'})
        for image in entry.find_all('img'):
            images.append(image.get('src'))
    return images


def _downloader(urls):
    ext = urls[-1].split('.')[-1]
    count = len(urls)
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    for n, url in enumerate(urls):
        print '(' + str(n+1) + '/' + str(count) + ')', 'Downloading', url
        file_name = str(n) + '.' + ext
        request = urllib2.Request(url, headers=hdr)
        u = urllib2.urlopen(request)
        f = open(file_name, 'wb')
        size = int(u.info().getheaders('Content-Length')[0])
        f.write(u.read(size))
        f.close()


def main(argv):
    url = _url_parser(argv[0])
    pages = _get_page_list(url)
    images = _get_images_url(pages)
    _downloader(images)    


if __name__ == '__main__':
    main(sys.argv[1:])