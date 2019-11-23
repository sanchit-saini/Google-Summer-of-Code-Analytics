# Google-Summer-of-Code-Analytics

[![Build Status](https://api.travis-ci.org/sanchit-saini/Google-Summer-of-Code-Analytics.svg?branch=master)](https://travis-ci.org/sanchit-saini/Google-Summer-of-Code-Analytics)

Helps GSoC candidates to shortlist organization instead searching and reviewing details of organizations manually.
Currently this project provides the csv file of every year from 2009 - 2019 which are present under the `stats` directory.
Every csv file contains name of the organization `name`, What they do `tagline`, What technologies are they actually using `technologies`, How many slots they had in a particular year `slots`.

If you want to know how many times a particular organization got selected for GSoC currently this can be done via sqlite
```
1. sqlite3 Database/gsoc_records.db
2.
For Detailed View : SELECT name,tagline,technologies,slots,year FROM records WHERE name = "Organization name from csv";
For Minimal View : SELECT COUNT(*) FROM records WHERE name = "Organization name from csv";
```
For example, let's search how many time `Python Software Foundation` got selected for GSoC
```
❯❯❯ sqlite3 Database/gsoc_records.db
sqlite❯ SELECT name,tagline,technologies,slots,year FROM records WHERE name = "Python Software Foundation";
Python Software Foundation|||25|2009
Python Software Foundation|||31|2010
Python Software Foundation|||30|2011
Python Software Foundation|||26|2012
Python Software Foundation|||18|2013
Python Software Foundation|||21|2014
Python Software Foundation|||62|2015
Python Software Foundation|Python is programming language popular among scientists and more.|python,mercurial|49|2016
Python Software Foundation|Python is a programming language used by scientists & software developers alike.|python|29|2017
Python Software Foundation|Python is a programming language used by software developers and scientists.|python|14|2018
Python Software Foundation|Python is a programming language used by software developers and scientists.|python|30|2019

sqlite❯ SELECT COUNT(*) FROM records WHERE name = "Python Software Foundation";
11

```


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

## Future Goals

- [ ] Interface to interact with a database to retrieve all the details which might be helpful for building apps on top of this interface