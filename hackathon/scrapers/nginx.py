from hackathon.scrapers.base import BaseScraper

class NginxScraper(BaseScraper):
    def __init__(self, host_regex, include_ingress=True, include_egress=True):
        BaseScraper.__init__(self)
        self.__regex = host_regex + '| parse regex "HTTP/.+?\\" (?<status_code>\d+)"'
        self.__include_ingress = include_ingress
        self.__include_egress = include_egress

    def get_good_query_in(self):
        if self.__include_ingress:
            return self.__regex + '| parse regex ": (?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | where status_code < 400 | count by ip, _sourceHost'
        else:
            return ''

    def get_warning_query_in(self):
        if self.__include_ingress:
            return self.__regex + '| parse regex ": (?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | where status_code < 500 | where status_code >= 400 | count by ip, _sourceHost'
        else:
            return ''

    def get_bad_query_in(self):
        if self.__include_ingress:
            return self.__regex+ '| parse regex ": (?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | where status_code >= 500 | count by ip, _sourceHost'
        else:
            return ''

    def get_good_query_out(self):
        if self.__include_egress:
            return self.__regex + '| parse regex "(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):" | where status_code < 400 | count by ip, _sourceHost'
        else:
            return ''

    def get_warning_query_out(self):
        if self.__include_egress:
            return self.__regex + '| parse regex "(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):" | where status_code < 500 | where status_code >= 400 | count by ip, _sourceHost'
        else:
            return ''
    def get_bad_query_out(self):
        if self.__include_egress:
            return self.__regex + '| parse regex "(?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):" | where status_code >= 500 | count by ip, _sourceHost'
        else:
            return ''
    
