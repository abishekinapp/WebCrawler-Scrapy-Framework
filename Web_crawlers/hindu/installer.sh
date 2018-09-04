#!/bin/bash

cd /etc
source ./bash.bashrc
source /usr/local/bin/virtualenvwrapper.sh #opening virstualenv for running scrapy

#directory of the project
cd /home/inapp/abishek_Training/phase_3/Web_crawlers/hindu 

#command to start crawling the spider
scrapy crawl crawl_spider