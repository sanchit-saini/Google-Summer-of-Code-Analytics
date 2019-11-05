# Google-Summer-of-Code-Analytics

Helps GSoC candidates to shortlist organization instead searching and reviewing details of organizations manually.
Currently this project provides the csv file of every year from 2009 - 2019 which are present under the `stats` directory.
Every csv file contains name of the organization `name`, What they do `tagline`, What technologies are they actually using `technologies`, How many slots they had in a particular year `slots`.


## Project Structure
```
Project Root
├── Database
│   └── gsoc_records.db         : records from 2009 - 2019
├── src
│   ├── config
│   ├── csv_generator.py        : script to transfrom records from db to csv
│   ├── DatabaseHelper.py       : helper class to communicate between db and Scraper
│   ├── Records.py              : records ORM 
│   └── Scrapper.py             : Scrape data 
└── stats                       : csv files
    └── *.csv
````