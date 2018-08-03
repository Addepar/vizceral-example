from hackathon.scrapers.base import BaseScraper

class RepgenScraper(BaseScraper):
    def get_good_query_in(self):
        return '_sourceCategory=kubernetes/prod/amp/reportgeneration/* | parse regex "\[\{ip=(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})}" | count by ip, _sourcehost'

    def post_process(self, edges):
        for edge in edges:
            edge.to_ip = 'repgen'
        return edges
