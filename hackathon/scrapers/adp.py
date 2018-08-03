from hackathon.scrapers.base import BaseScraper

class AdpScraper(BaseScraper):
    def __init__(self, host_regex):
        BaseScraper.__init__(self)
        self.__regex = host_regex

    def get_good_query_in(self):
        return self.__regex + ' AND "https://data.addepar.com" | parse regex "(?<ip>data.addepar.com)" | count by ip, _sourceHost'

    def get_good_query_out(self):
        return self.__regex + ' AND "account update notifications" | parse "Publishing * account" as notifications | "kafka" as ip | sum (notifications) as _count group ip, _sourceHost'
