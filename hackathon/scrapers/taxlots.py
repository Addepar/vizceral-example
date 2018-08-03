from hackathon.scrapers.base import BaseScraper

class TaxlotScraper(BaseScraper):
    def get_good_query_in(self):
        return '_sourceHost=taxlot*.prod.addepar.com AND "TaxLotDataGrpcServiceImpl: Total" | parse regex "Total (?<taxlots>\d+) " | parse regex "\[\{client=.+?/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | sum(taxlots) as _count by ip, _sourceHost | where _count != 0'
    def post_process(self, edges):
        for edge in edges:
            edge.good_volume /= 1000
            edge.warning_volume /= 1000
            edge.bad_volume /= 1000
        return edges
