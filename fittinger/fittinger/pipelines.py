# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib
import re
import os
import json


class FittingerPipeline(object):
    def __init__(self):
        self.out_dir = 'out/'
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

    def process_item(self, item, spider):
        item_id = re.search('^.*/(\d*)$', item['link']).group(1)
        url = 'http:' + item['images'][0]
        os.makedirs(self.out_dir + item_id)
        urllib.urlretrieve(url, self.out_dir + item_id + '/' + item_id + ".jpg")
        with open(self.out_dir + item_id + '/info.json', 'w') as outfile:
            json.dump(dict(item), outfile)
        return item
