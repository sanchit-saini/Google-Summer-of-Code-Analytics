#!/usr/bin/python
import sys
import getopt
import logging
from YearSupport import *
from DatabaseHelper import *
from urllib.request import urlopen
from bs4 import BeautifulSoup

logging.basicConfig(format='%(module)s : %(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class Scrapper:

    def __init__(self, base_url, year, year_support):
        self.year = int(year)
        self.base_url = base_url
        self.year_support = year_support
        logger.info('Initialized base URL : %s', self.base_url)

    def init_selectors(self, **kwds):

        if self.year_support.check_year_support(self.year):
            self.master_ul = kwds['master_ul']
            self.organization_name = kwds['organization_name']
            self.organization_slots_ul = kwds['organization_slots_ul']

        else:
            self.master_ul = kwds['master_ul']
            self.organization_name = kwds['organization_name']
            self.organization_slots_ul = kwds['organization_slots_ul']
            self.organization_tagline = kwds['organization_tagline']
            self.organization_technologies_ul = kwds['organization_technologies_ul']

        logger.info('Selectors Initialized')

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

        ul = self.soup.select_one(self.master_ul)
        logger.info('Iterating organization li tags and parsing href')
        
        for li in ul.find_all('li'):
            links.append(li.find('a').get('href'))
        return links

    def for_each_organization(self, links, **action):

        logger.info('Parsing and Inserting individual record into DB')
        for index in range(0, len(links)):
            link = self.base_url + links[index]

            action['set_soup'](link)

            if self.year_support.check_year_support(self.year):
                action['db_insert'](
                    name=self.get_orgnization_name(),
                    slots=str(self.get_organization_slot_count()),
                    year=self.year
                )
                logger.info('\nName: %s\nSlots: %s\nYear: %d\n',
                             self.get_orgnization_name(), self.get_organization_slot_count(), self.year)

            else:
                action['db_insert'](
                    name=self.get_orgnization_name(),
                    tagline=self.get_orgnization_tagline(),
                    technologies=self.get_organization_technologies(),
                    year=self.year,
                    slots=self.get_organization_slot_count()
                )
                logger.info('\nName: %s\nTagline: %s\nTechnologies: %s\nSlots: %s\nYear: %d\n',
                             self.get_orgnization_name(), self.get_orgnization_tagline(),
                             self.get_organization_technologies(), self.get_organization_slot_count(),
                             self.year)

    def get_orgnization_name(self):
        return self.soup.select_one(self.organization_name).get_text()

    def get_orgnization_tagline(self):
        return self.soup.select_one(self.organization_tagline).get_text()

    def get_organization_technologies(self):
        technologies = []

        ul = self.soup.select_one(self.organization_technologies_ul)

        for li in ul.find_all('li'):
            technologies.append(li.get_text())

        return str(technologies)

    def get_organization_slot_count(self):
        ul = self.soup.select_one(self.organization_slots_ul)
        return str(len(ul.find_all('li')))


def main(argv):

    year_support = YearSupport()
    year = None

    def usage_msg():
        return 'Usage: ' + argv[0] + ''' [Options]\n
     Options:\n
     -h,--help show this help message and exit\n
     -d, --debug activate debug mode\n
     -y, --year=XXXX set year to scrap data, year should be between [''' + year_support.get_year_range() + ']'

    try:
        opts, args = getopt.getopt(argv[1:], 'hdy:', ['debug', 'year=', 'help'])

    except getopt.GetoptError:
        logger.warning(usage_msg())

    for opt, arg in opts:
        if opt == '-h':
            print(usage_msg())

        elif opt in ('-d', '--debug'):
            logger.setLevel(logging.DEBUG)

        elif opt in ('-y', '--year'):
            year = arg

    if year == None:
        logger.warning(usage_msg())
        exit(0)

    if year_support.check_year(int(year)) == None:
        logger.warning('Out of year range: %s\nSupported year range : %s', year, year_support.get_year_range())
        exit(1)

    if year_support.check_year_support(int(year)):
        selectors = {
            'base_url': 'https://www.google-melange.com',
            'url': 'https://www.google-melange.com/archive/gsoc/' + year,
            'master_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul.mdl-list',
            'organization_name': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > h3',
            'organization_slots_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul'
        }

    else:
        selectors = {
            'base_url': 'https://summerofcode.withgoogle.com',
            'url': 'https://summerofcode.withgoogle.com/archive/' + year + '/organizations/',
            'master_ul': 'body > main > section > div > ul',
            'organization_name': 'body > div > div > div > h3',
            'organization_slots_ul': '#projects > div > ul',
            'organization_tagline': 'body > main > section.page-organizations-detail__details > div > div > div.org__long-description-wrapper > h4',
            'organization_technologies_ul': 'body > main > section.page-organizations-detail__details > div > div > div:nth-child(2) > md-card > div > div:nth-child(4) > ul'
        }

    sp = Scrapper(selectors['base_url'], year, year_support)
    sp.init_selectors(**selectors)
    sp.set_soup(selectors['url'])
    links = sp.get_organization_links()
    db_helper = DatabaseHelper()
    sp.for_each_organization(links, db_insert=db_helper.insert, set_soup=sp.set_soup)


if __name__ == '__main__':
    main(sys.argv)
