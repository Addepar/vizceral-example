from hackathon.scrapers.base import BaseScraper

class AdiaScraper(BaseScraper):
    def __init__(self, host_regex):
        BaseScraper.__init__(self)
        self.__regex = host_regex

    def get_good_query_in(self):
        return self.__regex + ' AND log_class=*NotificationDataService | parse "fetched [*] GFFs" as gffs | "batu1.prod.addepar.com" as ip | count by ip, _sourceHost'

    def get_bad_query_in(self):
        return self.__regex + ' AND "Finished processing status" | "batu1.prod.addepar.com" as ip | parse "error=*," as err | sum (err) as _count group ip, _sourceHost'
