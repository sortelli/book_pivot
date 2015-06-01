import lxml.etree as ET
import yaml
import sys
import os

class CXML:
  def __init__(self, dzc_file, config):
    self.dzc_root = ET.parse(dzc_file).getroot()
    self.name     = config['name']
    self.facets   = config['facets']
    self.items    = map(lambda item: item.attrib, self.dzc_root[0])

  def save(self, cxml_file):
    xmlns = {
      None: 'http://schemas.microsoft.com/collection/metadata/2009',
      'p':  'http://schemas.microsoft.com/livelabs/pivot/collection/2009'
    }

    collection = ET.Element('{{{0}}}Collection'.format(xmlns[None]), nsmap = xmlns)

    collection.set('SchemaVersion', '1')
    collection.set('Name',          self.name)

    facet_categories = ET.SubElement(collection, 'FacetCategories')
    items            = ET.SubElement(collection, 'Items')

    self.add_facet_categories(facet_categories, xmlns['p'])

    print(ET.tostring(collection, pretty_print = True))

  def add_facet_categories(self, facet_categories, pivot_ns):
    is_filter_visible = '{{{0}}}IsFilterVisible'   .format(pivot_ns)
    is_wheel_visible  = '{{{0}}}IsWordWheelVisible'.format(pivot_ns)

    for facet in self.facets:
      node = ET.SubElement(facet_categories, 'FacetCategory')
      node.set('Name', facet['name'])
      node.set('type', facet['type'])

      if not facet['filter']:
        node.set(is_filter_visible, 'false')
        node.set(is_wheel_visible,  'false')

os.chdir(os.path.dirname(__file__) if os.path.dirname(__file__) else '.')
config = yaml.load(open('books_config.yml', 'r'))
cxml   = CXML('collection/books.dzc', config)
cxml.save('books.cxml')
