import json,os,logging
from hindu.items import HinduItem
from scrapy.exceptions import DropItem
from hindu.spiders.hindu_spider import setup_logger
#import logging
from scrapy.exporters import JsonItemExporter

logger = setup_logger('logger', 'Log.txt')

dir_path = os.getcwd()+'/rules.json'
with open(dir_path, 'r') as f:
    rules_json = json.load(f)

#This is the pipeline used to select the required data alone
class HinduPipeline(object):
   
    #Funtion used to initialise exporter
    def __init__(self):
        self.file = open(rules_json["output_file"], 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    #Function in which the extracted data are selected and a wriiten into a output file
    def process_item(self, item, spider):
        if item['old_post']==0:
            raise DropItem("Droped Old Post : %s" % item)

        if not(item['title']):
            logger.log(logging.ERROR, "Title not present")
            logger.log(logging.WARNING, "Item Droped")
            raise DropItem("Missing title in %s" % item)

        elif not(item['content']):
            logger.log(logging.ERROR, "Content not present")
            logger.log(logging.WARNING, "Item Droped")
            raise DropItem("Missing content in %s" % item)

        elif not(item['publish_date']):
            logger.log(logging.ERROR, "Published_date not present")
            logger.log(logging.WARNING, "Item Droped")
            raise DropItem("Missing publish date in %s" % item)

        else :
            self.exporter.fields_to_export = ['title','subtitle','content','image_details','publish_date','modified_date','created_date','link']
            self.exporter.export_item(item)
            logger.log(logging.INFO, "Got a NEWS")
            if not(item['subtitle']):logger.log(logging.WARNING, "Subtitle not present")
            elif not(item['image_details']):logger.log(logging.WARNING, "Image not present")
            elif not(item['created_date']):logger.log(logging.WARNING, "Modified_date not present")
            return item              
