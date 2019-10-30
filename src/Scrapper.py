#!/usr/bin/python
import sys
import getopt
import logging
from DatabaseHelper import *
from urllib.request import urlopen
from bs4 import BeautifulSoup

logging.basicConfig(format='%(module)s : %(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class Scrapper:

    def __init__(self, base_url, year):
        self.year = int(year)
        self.base_url = base_url
        logger.info('Initialized base URL : %s', self.base_url)

    def init_selectors(self, **kwds):
        self.selectors = kwds
        logger.info('Initialized Selectors')
        for key in self.selectors:
            logger.info('%s : %s', key, self.selectors[key])

    def set_soup(self, url):

        try:
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            self.soup = soup

        except Exception:
            import traceback
            logger.error(traceback.format_exc())

    def get_organization_links(self):
        links = []

        ul = self.soup.select_one(self.selectors['master_ul'])
        logger.info('Iterating organization li tags and parsing href')
        
        for li in ul.find_all('li'):
            links.append(li.find('a').get('href'))
        return links

    def for_each_organization(self, links, db_insert):

        logger.info('Parsing and Inserting individual record into DB')
        for index in range(0, len(links)):
            link = self.base_url + links[index]

            self.set_soup(link)

            db_insert(
                name=self.get_orgnization_name(),
                tagline=self.get_orgnization_tagline(),
                technologies=self.get_organization_technologies(),
                year=self.year,
                slots=self.get_organization_slot_count()
            )
            logger.info('\nName: %s\nTagline: %s\nTechnologies: %s\nSlots: %d\nYear: %d\n',
                            self.get_orgnization_name(), self.get_orgnization_tagline(),
                            self.get_organization_technologies(), self.get_organization_slot_count(),
                            self.year)

    def get_orgnization_name(self):
        return self.soup.select_one(self.selectors['organization_name']).get_text()

    def get_orgnization_tagline(self):
        if 'organization_tagline' in self.selectors:
            return self.soup.select_one(self.selectors['organization_tagline']).get_text()
        return ''

    def get_organization_technologies(self):
        if 'organization_technologies_ul' in self.selectors:
            technologies = []

            ul = self.soup.select_one(self.selectors['organization_technologies_ul'])

            for li in ul.find_all('li'):
                technologies.append(li.get_text())

            return ','.join(technologies)
        return ''

    def get_organization_slot_count(self):
        ul = self.soup.select_one(self.selectors['organization_slots_ul'])
        return len(ul.find_all('li'))


def main(argv):

    year = 0
    old_base_url_start_year = 2009
    old_base_url_end_year = 2015
    new_base_url_end_year = 2019

    def usage_msg():
        return '''\nUsage: {}  [Options]\n
            Options:\n
            -h,--help show this help message and exit\n
            -d, --debug activate debug mode\n
            -y, --year=XXXX set year to scrap data, year should be between [ {} - {} ]'''\
        .format(argv[0], old_base_url_start_year, new_base_url_end_year)

    try:
        opts, args = getopt.getopt(argv[1:], 'hdy:', ['debug', 'year=', 'help'])

    except getopt.GetoptError:
        logger.warning(usage_msg())

    for opt, arg in opts:
        if opt == '-h':
            print(usage_msg())
            exit(0)

        elif opt in ('-d', '--debug'):
            logger.setLevel(logging.DEBUG)

        elif opt in ('-y', '--year'):
            year = int(arg)

    if year == 0:
        logger.warning(usage_msg())
        exit(0)

    if year < old_base_url_start_year or year > new_base_url_end_year:
        logger.warning('\nOut of year range: %s\nSupported year range : %d - %d', year, old_base_url_start_year, new_base_url_end_year )
        exit(1)

    if year >= old_base_url_start_year and year <= old_base_url_end_year:
        selectors = {
            'base_url': 'https://www.google-melange.com',
            'url': 'https://www.google-melange.com/archive/gsoc/{}'.format(year),
            'master_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul.mdl-list',
            'organization_name': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > h3',
            'organization_slots_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul'
        }

    else:
        selectors = {
            'base_url': 'https://summerofcode.withgoogle.com',
            'url': 'https://summerofcode.withgoogle.com/archive/{}/organizations/'.format(year),
            'master_ul': 'body > main > section > div > ul',
            'organization_name': 'body > div > div > div > h3',
            'organization_slots_ul': '#projects > div > ul',
            'organization_tagline': 'body > main > section.page-organizations-detail__details > div > div > div.org__long-description-wrapper > h4',
            'organization_technologies_ul': 'body > main > section.page-organizations-detail__details > div > div > div:nth-child(2) > md-card > div > div:nth-child(4) > ul'
        }

    sp = Scrapper(selectors['base_url'], year)
    sp.init_selectors(**selectors)
    sp.set_soup(selectors['url'])

    links = sp.get_organization_links()
    db_helper = DatabaseHelper()
    sp.for_each_organization(links, db_helper.insert)


if __name__ == '__main__':
    main(sys.argv)
