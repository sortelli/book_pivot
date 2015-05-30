#!/usr/bin/env python

import yaml
import sys
import os
import urllib2
import time
from amazon.api import AmazonAPI

# Change to script directory
os.chdir(os.path.dirname(sys.argv[0]))

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

books = Books('config.yml')

for isbn in sys.argv[1:]:
  try:
    book = books.lookup(isbn)

    with open('raw_data/{0}.yml'.format(isbn), 'w') as out:
      out.write(yaml.dump(book, default_flow_style = False))

    with open('raw_data/{0}.jpg'.format(isbn), 'wb') as out:
      data = urllib2.urlopen(book['image_url']).read()
      out.write(data)

    print "Got data for {0}".format(isbn)

  except:
    print "Unexpected error on {0}".format(isbn), sys.exc_info()[0]

  time.sleep(0.5)
