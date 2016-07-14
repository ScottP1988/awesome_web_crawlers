#!/usr/local/bin/python

import urllib2
import sys
import ssl
import bs4


def _get_content(case_number):
    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    num = 'appReceiptNum=' + case_number
    request = urllib2.Request(url, data=num)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    content = urllib2.urlopen(request, context=ctx)
    return content.read()


def _fetch_case_info(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    target_div = soup.find('div', attrs={'class': 'rows text-center'})
    return target_div.find('h1').getText(), target_div.find('p').getText()


def main(argv):
    case_number = argv[0]
    content = _get_content(case_number)
    status, info = _fetch_case_info(content)
    print('Case number: {0}\nStatus: {1}\nDetails: {2}'.format(case_number, status, info))

if __name__ == '__main__':
    main(sys.argv[1:])
