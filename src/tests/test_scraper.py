
import os
import sys
import unittest

base_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '../scraper')
sys.path.append(base_path)

import cli as Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        year = 2016
        selectors = Scraper.get_selectors(year)
        self.scraper = Scraper.get_scraper(selectors, year)

    def test_get_organization_links(self):
        self.assertEqual(self.scraper.get_organization_links()[0],
                         '/archive/2016/organizations/5429283996565504/')

    def test_get_orgnization_name(self):
        uri = self.scraper.get_organization_links()[0]
        link = self.scraper.base_url + uri
        self.scraper.set_soup(link)
        self.assertEqual(self.scraper.get_orgnization_name(),
                         '52°North Initiative for Geospatial Open Source Software GmbH')

    def test_get_orgnization_tagline(self):
        uri = self.scraper.get_organization_links()[0]
        link = self.scraper.base_url + uri
        self.scraper.set_soup(link)
        self.assertEqual(self.scraper.get_orgnization_tagline(),
                         '52°North works on innovative ideas and technologies in geoinformatics')

    def test_get_organization_technologies(self):
        uri = self.scraper.get_organization_links()[0]
        link = self.scraper.base_url + uri
        self.scraper.set_soup(link)
        self.assertEqual(self.scraper.get_organization_technologies(),
                         'javascript,java,ogc standards,web services')

    def test_get_organization_slot_count(self):
        uri = self.scraper.get_organization_links()[0]
        link = self.scraper.base_url + uri
        self.scraper.set_soup(link)
        self.assertEqual(self.scraper.get_organization_slot_count(), 3)


if __name__ == "__main__":
    unittest.main()
