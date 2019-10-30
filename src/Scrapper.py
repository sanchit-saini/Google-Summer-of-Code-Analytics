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

    def __init__(self, baseUrl, year, yearSupport):
        self.year = int(year)
        self.baseUrl = baseUrl
        self.yearSupport = yearSupport
        logger.info('Initialized base URL : %s', self.baseUrl)

    def initSelectors(self, **kwds):

        if self.yearSupport.checkYearSupport(self.year):
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

    def setSoup(self, url):

        try:
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            self.soup = soup

        except Exception:
            import traceback
            logger.error(traceback.format_exc())

    def getOrganizationLinks(self):
        links = []

        ul = self.soup.select_one(self.master_ul)
        logger.info('Iterating organization li tags and parsing href')
        
        for li in ul.find_all('li'):
            links.append(li.find('a').get('href'))
        return links

    def forEachOrganization(self, links, **action):

        logger.info('Parsing and Inserting individual record into DB')
        for index in range(0, len(links)):
            link = self.baseUrl + links[index]

            action['setSoup'](link)

            if self.yearSupport.checkYearSupport(self.year):
                action['dbInsert'](
                    name=self.getOrgnizationName(),
                    slots=str(self.getOrganizationSlotCount()),
                    year=self.year
                )
                logger.info('\nName: %s\nSlots: %s\nYear: %d\n',
                             self.getOrgnizationName(), self.getOrganizationSlotCount(), self.year)

            else:
                action['dbInsert'](
                    name=self.getOrgnizationName(),
                    tagline=self.getOrgnizationTagline(),
                    technologies=self.getOrganizationTechnologies(),
                    year=self.year,
                    slots=self.getOrganizationSlotCount()
                )
                logger.info('\nName: %s\nTagline: %s\nTechnologies: %s\nSlots: %s\nYear: %d\n',
                             self.getOrgnizationName(), self.getOrgnizationTagline(),
                             self.getOrganizationTechnologies(), self.getOrganizationSlotCount(),
                             self.year)

    def getOrgnizationName(self):
        return self.soup.select_one(self.organization_name).get_text()

    def getOrgnizationTagline(self):
        return self.soup.select_one(self.organization_tagline).get_text()

    def getOrganizationTechnologies(self):
        technologies = []

        ul = self.soup.select_one(self.organization_technologies_ul)

        for li in ul.find_all('li'):
            technologies.append(li.get_text())

        return str(technologies)

    def getOrganizationSlotCount(self):
        ul = self.soup.select_one(self.organization_slots_ul)
        return str(len(ul.find_all('li')))


def main(argv):

    yearSupport = YearSupport()
    year = None

    def usageMsg():
        return 'Usage: ' + argv[0] + ''' [Options]\n
     Options:\n
     -h,--help show this help message and exit\n
     -d, --debug activate debug mode\n
     -y, --year=XXXX set year to scrap data, year should be between [''' + yearSupport.getYearRange() + ']'

    try:
        opts, args = getopt.getopt(argv[1:], 'hdy:', ['debug', 'year=', 'help'])

    except getopt.GetoptError:
        logger.warning(usageMsg())

    for opt, arg in opts:
        if opt == '-h':
            print(usageMsg())

        elif opt in ('-d', '--debug'):
            logger.setLevel(logging.DEBUG)

        elif opt in ('-y', '--year'):
            year = arg

    if year == None:
        logger.warning(usageMsg())
        exit(0)

    if yearSupport.checkYear(int(year)) == None:
        logger.warning('Out of year range: %s\nSupported year range : %s', year, yearSupport.getYearRange())
        exit(1)

    if yearSupport.checkYearSupport(int(year)):
        dict = {
            'baseUrl': 'https://www.google-melange.com',
            'url': 'https://www.google-melange.com/archive/gsoc/' + year,
            'master_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul.mdl-list',
            'organization_name': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > h3',
            'organization_slots_ul': 'body > div > main > div > div.main.mdl-cell.mdl-cell--8-col.mdl-card.mdl-shadow--4dp > ul'
        }

    else:
        dict = {
            'baseUrl': 'https://summerofcode.withgoogle.com',
            'url': 'https://summerofcode.withgoogle.com/archive/' + year + '/organizations/',
            'master_ul': 'body > main > section > div > ul',
            'organization_name': 'body > div > div > div > h3',
            'organization_slots_ul': '#projects > div > ul',
            'organization_tagline': 'body > main > section.page-organizations-detail__details > div > div > div.org__long-description-wrapper > h4',
            'organization_technologies_ul': 'body > main > section.page-organizations-detail__details > div > div > div:nth-child(2) > md-card > div > div:nth-child(4) > ul'
        }

    sp = Scrapper(dict['baseUrl'], year, yearSupport)
    sp.initSelectors(**dict)
    sp.setSoup(dict['url'])
    links = sp.getOrganizationLinks()
    dbHelper = DatabaseHelper()
    sp.forEachOrganization(links, dbInsert=dbHelper.insert, setSoup=sp.setSoup)


if __name__ == '__main__':
    main(sys.argv)
