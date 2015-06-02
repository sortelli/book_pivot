#!/usr/bin/env python

import yaml
import sys
import os
import subprocess
import urllib2
import time

from books import Books
from cxml  import CXML

os.chdir(os.path.dirname(sys.argv[0]))

if not os.path.exists('raw_data'):
  os.mkdir('raw_data')

if not os.path.exists('collection'):
  os.mkdir('collection')

os.chdir('collection')

books = Books('../config.yml')

for isbn in sys.argv[1:]:
  if os.path.exists(isbn + '.dzi'):
    print "Item is already in collection: " + isbn
    continue

  try:
    book     = books.lookup(isbn)
    yml_file = '../raw_data/{0}.yml'.format(isbn)
    jpg_file = '../raw_data/{0}.jpg'.format(isbn)

    with open(yml_file, 'w') as out:
      out.write(yaml.dump(book, default_flow_style = False))

    with open(jpg_file, 'wb') as out:
      data = urllib2.urlopen(book['image_url']).read()
      out.write(data)

    subprocess.call("makedeepzoom -c 'books.dzc' '{0}'".format(jpg_file), shell=True)

    print "Added {0}, {1}".format(isbn, book['title'])

  except:
    print "Unexpected error on {0}".format(isbn), sys.exc_info()[0]

  time.sleep(0.5)

os.chdir('..')
config = yaml.load(open('books_config.yml', 'r'))
cxml   = CXML('collection/books.dzc', 'raw_data', config)
cxml.save('books.cxml')
