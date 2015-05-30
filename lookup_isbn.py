#!/usr/bin/env python

import yaml
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

book = Books('config.yml').lookup('9781449389734')
print yaml.dump(book, default_flow_style = False)
