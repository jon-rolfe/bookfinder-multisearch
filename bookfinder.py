#!/usr/bin/env python

"""
Usage: ./bookfinder.py /path/to/book/list
Bookfinder.com is great, but the lack of multi-search
functionality makes getting good deals on $largenum of
books annoying.
"""

import os
import sys
import argparse
import signal
from lxml import html
import requests


def main():
    """Handles user input."""
    # parse them arguments
    cli_parse = argparse.ArgumentParser(
        description='Performs a multi-search on bookfinder.com.')

    cli_parse.add_argument('path', action='store',
                           help='path to your list of books')

    args = cli_parse.parse_args()

    # validate file presence/validity
    if not os.path.isfile(args.path):
        print 'invalid path'
        close(True)

    listpath = open(args.path, 'r')
    booklist = []
    for line in listpath:
        booklist.append(line.strip())

    # done grabbing from the file, so we can close it
    listpath.close()

    # TODO: start loop here
    for book in booklist:
        print '%s:' % book

        payload = {
            'author': '',
            'title': book,
            'submitBtn': 'Search',
            'new_used': '*',
            'destination': 'us',
            'currency': 'USD',
            'binding': '*',
            'isbn': '',
            'keywords': '',
            'minprice': '',
            'maxprice': '',
            'min_year': '',
            'max_year': '',
            'mode': 'advanced',
            'st': 'sr',
            'ac': 'qr'
        }

        # now start the actual searches
        request = requests.get('http://www.bookfinder.com/search/', params=payload)

        # select the first result from the list and get that page
        parser = html.fromstring(request.text)
        request = requests.get(parser.xpath('//*[@id="bd"]/ul/li[1]/span/a/@href')[0])

        # using some xpath magic, get the useful stuff from the page
        parser = html.fromstring(request.text)

        newprice = parser.xpath(
            '//*[@id="bd"]/table/tr/td[1]/table/tr[2]/td[4]/div/span/a/text()')[0]
        newseller = parser.xpath(
            '//*[@id="bd"]/table/tr/td[1]/table/tr[2]/td[2]//a/img/@src')[0]
        newseller = newseller[58:].partition('.')[0].replace('_', ' ').capitalize()
        newlink = parser.xpath(
            '//*[@id="bd"]/table/tr/td[1]/table/tr[2]/td[4]/div/span/a/@href')[0]
        newlink = shorten(newlink)
        print '\tNew: %s at %s - %s' % (newprice, newseller, newlink)

        usedprice = parser.xpath(
            '//*[@id="bd"]/table/tr/td[5]/table/tr[2]/td[4]/div/span/a/text()')[0]
        usedseller = parser.xpath(
            '//*[@id="bd"]/table/tr/td[5]/table/tr[2]/td[2]/span[2]/a/img/@src')[0]
        usedseller = usedseller[58:].partition('.')[0].replace('_', ' ').capitalize()
        usedlink = parser.xpath(
            '//*[@id="bd"]/table/tr/td[5]/table/tr[2]/td[4]/div/span/a/@href')[0]
        usedlink = shorten(usedlink)
        print '\tUsed: %s at %s - %s' % (usedprice, usedseller, usedlink)


def shorten(link):
    """The store links are stupid long, so shorten them."""
    params = {
        'format': 'simple',
        'url': link
    }
    # is.gd is used because it doesn't require auth/is free/no ads
    return requests.get('https://is.gd/create.php', params=params).content


def close(error):
    """Handles sigint/normal program exit"""
    if error is False:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    # make a SIGINT handler for ctrl-c, etc
    signal.signal(signal.SIGINT, exit)
    # call main
    main()
