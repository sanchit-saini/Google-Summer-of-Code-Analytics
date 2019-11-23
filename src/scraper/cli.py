#!/usr/bin/python
import sys
import logging
import argparse
import records
import database_helper
from bs4 import BeautifulSoup
from urllib.request import urlopen

old_base_url_start_year = 2009
old_base_url_end_year = 2015
new_base_url_end_year = 2019
logging.basicConfig(format='%(module)s : %(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class Scraper:
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
        logger.info('Parsing and Inserting individual record in Session')
        for index in range(0, len(links)):
            link = self.base_url + links[index]

            self.set_soup(link)

            db_insert(
                records.Records(
                    self.get_orgnization_name(),
                    self.get_organization_slot_count(),
                    self.get_orgnization_tagline(),
                    self.get_organization_technologies(),
                    self.year
                )
            )
            logger.info('\nName: %s\nTagline: %s\nTechnologies: %s\
                        \nSlots: %d\nYear: %d\n',
                        self.get_orgnization_name(),
                        self.get_orgnization_tagline(),
                        self.get_organization_technologies(),
                        self.get_organization_slot_count(),
                        self.year)

    def get_orgnization_name(self):
        return self.soup.select_one(
            self.selectors['organization_name']
        ).get_text()

    def get_orgnization_tagline(self):
        if 'organization_tagline' in self.selectors:
            return self.soup.select_one(
                self.selectors['organization_tagline']
            ).get_text()
        return ''

    def get_organization_technologies(self):
        if 'organization_technologies_ul' in self.selectors:
            technologies = []

            ul = self.soup.select_one(
                self.selectors['organization_technologies_ul'])

            for li in ul.find_all('li'):
                technologies.append(li.get_text())

            return ','.join(technologies)
        return ''

    def get_organization_slot_count(self):
        ul = self.soup.select_one(self.selectors['organization_slots_ul'])
        return len(ul.find_all('li'))


def get_selectors(year):
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
    return selectors


def get_scraper(selectors, year):
    sp = Scraper(selectors['base_url'], year)
    sp.init_selectors(**selectors)
    sp.set_soup(selectors['url'])
    return sp


def get_database_helper():
    db_helper = database_helper.DatabaseHelper()
    db_helper.create_database()
    return db_helper


def main(argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', '-d',
                            action='store_true',
                            default=False,
                            help='activate debug mode')
    arg_parser.add_argument('year',
                            type=int,
                            help='scrape records for this year, range: {} - {}'
                            .format(old_base_url_start_year, new_base_url_end_year))
    args = arg_parser.parse_args()

    year = args.year
    debug_flag = args.debug

    if debug_flag is True:
        logger.setLevel(logging.DEBUG)

    if year < old_base_url_start_year or year > new_base_url_end_year:
        logger.warning('\nOut of year range: %s\
                        \nSupported year range : %d - %d',
                       year, old_base_url_start_year, new_base_url_end_year)
        exit(1)

    selectors = get_selectors(year)
    sp = get_scraper(selectors, year)
    db_helper = get_database_helper()
    links = sp.get_organization_links()
    sp.for_each_organization(links, db_helper.insert)


if __name__ == '__main__':
    main(sys.argv)
