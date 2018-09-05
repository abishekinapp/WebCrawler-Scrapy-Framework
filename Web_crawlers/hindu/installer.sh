
#!/bin/bash

#Installing virtualenv
python -m pip install --user virtualenv
#Creaeting virtualenv
python -m virtualenv env
#Activating virtualenv
source env/bin/activate
#Installing twisted for scrapy
pip install twisted
#Installing scrapy framework
pip install scrapy

var_path=$PWD # storing the curent working directory for future use
cd /etc
source ./bash.bashrc

#Redirecting to the Project for Running the spider
cd $var_path

#command for start Crawling
scrapy crawl crawl_spider
