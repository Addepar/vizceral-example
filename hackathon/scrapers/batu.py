from hackathon.scrapers.base import BaseScraper

class BatuScraper(BaseScraper):
    def __init__(self, host_regex):
        BaseScraper.__init__(self)
        self.__regex = host_regex

    def get_good_query_in(self):
        return self.__regex + ' AND "finished work item" | "kafka" as ip | count by ip, _sourceHost'
