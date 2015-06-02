#!/usr/bin/env python

import yaml
import sys
import os
import subprocess
import urllib2
import time
from amazon.api import AmazonAPI


class Books:
  def __init__(self, config_file):
    self.config = yaml.load(open(config_file, 'r'))
    self.amazon = AmazonAPI(
      self.config['aws_access_key_id'],
      self.config['aws_secret_key'],
      self.config['amazon_associate_tag']
    )

  def lookup(self, isbn):
    product = self.amazon.lookup(ItemId = isbn, IdType = 'ISBN', SearchIndex = "Books") 

    if isinstance(product, (list)):
      product = product[0]

    book = {
      '_name':            product.title,
      '_href':            product.offer_url,
      'title':            product.title,
      'image_url':        product.large_image_url,
      'sales_rank':       int(product.sales_rank),
      'price':            product.price_and_currency[0],
      'offer_url':        product.offer_url,
      'authors':          product.authors,
      'publisher':        product.publisher,
      'isbn':             isbn,
      'binding':          product.binding,
      'pages':            product.pages,
      'publication_date': product.publication_date,
      'list_price':       product.list_price[0]
    }

    return book

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
