from hackathon.scrapers.base import BaseScraper

class SnapshotScraper(BaseScraper):
    def get_good_query_in(self):
        return '_sourceHost=snap*.prod.addepar.com | parse regex "Total (?<snapshots>\d+) " | parse regex "\[\{client=.+?/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | sum(snapshots) as _count by ip, _sourceHost | where _count != 0'
    # def post_process(self, edges):
    #     for edge in edges:
    #         edge.good_volume /= 100
    #         edge.warning_volume /= 100
    #         edge.bad_volume /= 100
    #     return edges
