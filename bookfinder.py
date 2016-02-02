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
import logging
from lxml import html
import requests


def main():
    """Does most of the magic."""
    # parse them arguments
    cli_parse = argparse.ArgumentParser(
        description='Performs a multi-search on bookfinder.com.')

    cli_parse.add_argument('infile', action='store',
                           help='path to your list of books')

    cli_parse.add_argument('outfile', action='store',
                           help='path you want to output to')

    args = cli_parse.parse_args()

    # using logger to output to stdout + file; wipe file first
    open(args.outfile, 'w').close()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger('bookfinder')
    loghandler = logging.FileHandler(args.outfile)
    logger.addHandler(loghandler)

    # disable requests' logging, because we don't care
    logging.getLogger('requests').setLevel(logging.WARNING)

    # validate file presence/validity
    if not os.path.isfile(args.infile):
        logger.error('Invalid input file path.')
        close()

    # create array for the list o' books, grab line by line, encode to ascii
    listpath = open(args.infile, 'r')
    booklist = []
    for line in listpath:
        booklist.append(line.strip().decode('ascii', 'ignore'))

    # done grabbing from the file, so we can close it
    listpath.close()

    for book in booklist:
        logger.info('%s:', book)

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

        # get the best 3 results for new, then the best 3 for used
        for i in range(2, 5):
            try:
                newprice = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[1]/table/tr[%s]/td[4]/div/span/a/text()' % i)[0]
                newseller = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[1]/table/tr[%s]/td[2]//a/img/@src' % i)[0]
                newseller = newseller[58:].partition('.')[0].replace('_', ' ').capitalize()
                newlink = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[1]/table/tr[%s]/td[4]/div/span/a/@href' % i)[0]
                newlink = shorten(newlink)
                logger.info('\tNew: %s at %s - %s', newprice, newseller, newlink)
            except:
                break
        for i in range(2, 5):
            try:
                usedprice = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[5]/table/tr[%s]/td[4]/div/span/a/text()' % i)[0]
                usedseller = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[5]/table/tr[%s]/td[2]//a/img/@src' % i)[0]
                usedseller = usedseller[58:].partition('.')[0].replace('_', ' ').capitalize()
                usedlink = parser.xpath(
                    '//*[@id="bd"]/table/tr/td[5]/table/tr[%s]/td[4]/div/span/a/@href' % i)[0]
                usedlink = shorten(usedlink)
                logger.info('\tUsed: %s at %s - %s', usedprice, usedseller, usedlink)
            except:
                break


def shorten(link):
    """The store links are stupid long, so shorten them."""
    params = {
        'format': 'simple',
        'url': link
    }
    # is.gd is used because it doesn't require auth/is free/no ads
    return requests.get('http://is.gd/create.php', params=params).content


def close():
    """Handles sigint/unexpected program exit"""
    sys.exit(1)

if __name__ == "__main__":
    # make a SIGINT handler for ctrl-c, etc
    signal.signal(signal.SIGINT, close)
    # call main
    main()
