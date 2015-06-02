import lxml.etree as ET
import yaml
import sys
import os

class CXML:
  def __init__(self, dzc_file, data_dir, config):
    self.dzc_file = dzc_file
    self.data_dir = data_dir
    self.name     = config['name']
    self.facets   = config['facets']

    dzc_root = ET.parse(self.dzc_file).getroot()
    self.dzc_items = map(lambda item: item.attrib, dzc_root[0])

  def save(self, cxml_file):
    xmlns = {
      None: 'http://schemas.microsoft.com/collection/metadata/2009',
      'p':  'http://schemas.microsoft.com/livelabs/pivot/collection/2009'
    }

    collection = ET.Element('{{{0}}}Collection'.format(xmlns[None]), nsmap = xmlns)

    collection.set('SchemaVersion', '1')
    collection.set('Name',          self.name)

    facet_categories = ET.SubElement(collection, 'FacetCategories')
    self.add_facet_categories(facet_categories, xmlns['p'])

    items = ET.SubElement(collection, 'Items')
    items.set('ImgBase', self.dzc_file)
    self.add_items(items)

    print(ET.tostring(collection, pretty_print = True))

  def add_items(self, items):
    for item in self.dzc_items:
      data = self.get_item_data(item['Source'])
      node = ET.SubElement(items, 'Item')
      name = '#' + item['N']

      node.set('Img',  name)
      node.set('Id',   item['N'])
      node.set('Name', data.get('_name', name))
      node.set('Href', data.get('_href', '#'))

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

  def get_item_data(self, dzi_source):
    dzi_id    = os.path.splitext(os.path.basename(dzi_source))[0]
    data_file = os.path.join(self.data_dir, dzi_id + '.yml')

    with open(data_file, 'r') as yml:
      return yaml.load(yml)

os.chdir(os.path.dirname(__file__) if os.path.dirname(__file__) else '.')
config = yaml.load(open('books_config.yml', 'r'))
cxml   = CXML('collection/books.dzc', 'raw_data', config)
cxml.save('books.cxml')
