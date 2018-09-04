import scrapy,json,os
from hindu.items import HinduItem
import logging
import datetime

#Initialising  Items
item = HinduItem()

#Opening and Loading the rules.json file
dir_path = os.getcwd()+'/rules.json'
with open(dir_path, 'r') as f:
    rules_json = json.load(f)

#Funtion for initialising Logger
def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = setup_logger('logger', 'Log.txt')

#Spider used for scrapping news from the website
class news_spider(scrapy.Spider):
    name = "crawl_spider"
    logger.log(logging.INFO, "Entering Spider : new_spider ")

    #Function for defining start url
    def start_requests(self):

        urls = rules_json["url_allowed"]
        logger.log(logging.INFO, urls )

        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    #Fuction to check the domain
    def check_domain(self,link):
         
        allowed_domains = rules_json["allowed_domains"]

        for i in range (0,10):
            link = str(link)
            url= allowed_domains[i]
            if url in link :
                return 1
            else :
                return 0
    
    #Function to check the xpaths from the list of alternative xpaths given for a field
    def check_command(self,json,response,is_content):

        for i in range (0,2):
            if is_content == True:
                ex_data = response.xpath(json[i].replace('#', '"')).extract()
            else:
                ex_data = response.xpath(json[i].replace('#', '"')).extract_first()
            if not(ex_data):
                flag=0
                continue
            else:
                flag=1
                break
        if flag == 0:
            ex_data = ''
            return ex_data
        else :
            return ex_data

    #Function used to extract data from the specified path
    def extract_data(self,response):

        is_content = False
        item['link'] = response.request.url
        item['title'] = self.check_command(rules_json["title"],response,is_content)
        item['content'] = self.check_command(rules_json["content"],response,is_content = True)
        item['subtitle'] = self.check_command(rules_json["subtitle"],response,is_content)
        if not(item['subtitle']):
            item['subtitle']= ''    #The null value is replaced with empty string

        item['image_details'] = self.check_command(rules_json["image_details"],response,is_content)
        if not(item['image_details']):
            item['image_details']= ''     #The null value is replaced with empty string

        item['publish_date'] = self.check_command(rules_json["publish_date"],response,is_content)
        item['created_date'] = self.check_command(rules_json["created_date"],response,is_content)

        if not(item['created_date']):
            item['created_date']= ''
        

    #the following are the code to seprate the post which are older than 6 months 
    def check_old(self,created_date):

        a= created_date
        now = datetime.datetime.now()
        if created_date[0] != '':
            year = int(a[0])
            month = int(a[1])

            current_month = now.month
            current_year = now.year
            month_difference = current_month-month
            posts_MonthsOlder = rules_json["posts_MonthsOlder"]

            if current_month > posts_MonthsOlder :
                if year == current_year:
                    month_deadline = month_difference
                    if month > month_deadline: 
                        item['old_post']=1
                else:
                    item['old_post']=0
            else:
                if year == current_year or year == current_year-1 :
                    month_deadline = 12 - month_difference
                    if month > month_deadline:
                        item['old_post']=1
                else:
                    item['old_post']=0  


    #Funtion to extract all the links from the website and the urls are dirirected to Funtion news_parse for extracting data
    def parse(self, response):

        links = response.css('a::attr(href)').extract()
        logger.log(logging.INFO, "Extracted all a-Tags ")
        
        for link in links:
            logger.log(logging.DEBUG, "Iterating through the links ")
            
            check = self.check_domain(link)
            
            if check == 1 :
                logger.log(logging.DEBUG, "Entered the hindu webpage")
                logger.log(logging.INFO, "In the correct WEBPAGE")
                yield scrapy.Request(url = link, callback = self.news_parse)
            
            elif check == 0:
                logger.log(logging.CRITICAL, "Redirected to a wrong WEBPAGE")    
                                   
            
    #Funtion used to extract data from the urls passed from the funtion parse
    def news_parse(self, response):

            logger.log(logging.DEBUG, "extracting the content from the webpage")
            self.extract_data(response)
            created_date=item['created_date'].strip('="').split('-')
            self.check_old(created_date)

            yield item
     
            #The urls in the current page which leads to other news are extracted and passed to news_parse
            links = response.css('a::attr(href)').extract()
   
            for link in links:
                logger.log(logging.DEBUG, "Iterating through the links ")
                
                check = self.check_domain(link)
                if check == 1 :
                    logger.log(logging.DEBUG, "Entered the hindu webpage")
                    logger.log(logging.INFO, "In the correct WEBPAGE")
                    yield scrapy.Request(url = link, callback = self.news_parse)
                
                elif check == 0:
                    logger.log(logging.CRITICAL, "Redirected to a wrong WEBPAGE")
            
