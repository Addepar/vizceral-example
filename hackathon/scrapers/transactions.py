from hackathon.scrapers.base import BaseScraper

class TransactionScraper(BaseScraper):
    def get_good_query_in(self):
        return '_sourceHost=tx*.prod.addepar.com | parse regex "Total (?<taxlots>\d+) " | parse regex "\[\{client=.+?/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | sum(taxlots) as _count by ip, _sourceHost | where _count != 0'
    def post_process(self, edges):
        for edge in edges:
            edge.good_volume /= 10
            edge.warning_volume /= 10
            edge.bad_volume /= 10
        return edges
