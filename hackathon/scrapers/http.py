from hackathon.scrapers.base import BaseScraper

class HttpScraper(BaseScraper):
    def __init__(self, host_regex):
        BaseScraper.__init__(self)
        self.__regex = host_regex + ' AND HttpRequestLogFilter AND END_REQUEST '
        
    def get_good_query(self):
        return self.__regex + '| where status_code < 500 | count by ip, _sourceHost'
    
    def get_bad_query(self):
        return self.__regex + '| where status_code >= 500 | count by ip, _sourceHost'

    def post_process(self, edges):
        # If iverson6, change to 50-50 mslb-prod-ext
        # Hack because mslb-prod-ext doesn't put its own ip in...

        iverson_dict = {}
        for edge in edges:
            if edge.from_ip in ['10.0.0.124', '10.0.0.33']:
                iverson_dict[edge.to_ip] = {
                    'good': edge.good_volume,
                    'bad': edge.bad_volume
                }
        
        new_edges = []
        for edge in edges:
            if edge.from_ip in ['10.0.0.124', '10.0.0.33']:
                continue
            if edge.from_ip in ['10.0.0.124', '10.0.0.33']:
                iverson_traffic = iverson_dict.get(edge.to_ip, {})
                edge.good_volume += iverson_traffic.get('good', 0)
                edge.bad_volume += iverson_traffic.get('bad', 0)
            new_edges.append(edge)
            
        return new_edges
