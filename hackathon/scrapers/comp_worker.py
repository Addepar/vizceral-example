from hackathon.scrapers.base import BaseScraper

class CompWorkerScraper(BaseScraper):
    def get_good_query_in(self):
        return '_sourceHost=prodcompworker* AND "PathCalculationGrpcServiceImpl: Finished Compworker Job" | parse regex "\[\{client=.+?/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | count by ip, _sourceHost'

    def get_bad_query_in(self):
        return '_sourceHost=prodcompworker* AND "PathCalculationGrpcServiceImpl: Exception running job" | parse regex "\[\{client=.+?/(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | count by ip, _sourceHost'
