from pluto.sumologic.sumo_search import SumoSearch
from hackathon.models import Node, Edge

import re

class BaseScraper:
    def __init__(self):
        self.__sumo = SumoSearch()

    def __process_in(self, query, cache, start_time, end_time):
        if not query:
            return
        print(query)
        results = self.__sumo.search_job(query, start_time, end_time)
        for result in results:
            from_ip = result['ip'].split(', ')[-1]
            to_ip = result['_sourcehost']

            # if not re.match('^\d+\.\d+\.\d+\.\d+$', from_ip):
            #     continue
            key = (from_ip, to_ip)
            cache[key] = cache.get(key, 0) + int(float(result['_count']))
    
    def __process_out(self, query, cache, start_time, end_time):
        if not query:
            return
        print(query)
        results = self.__sumo.search_job(query, start_time, end_time)
        for result in results:
            from_ip = result['_sourcehost']
            to_ip = result['ip'].split(', ')[-1]

            # if not re.match('^\d+\.\d+\.\d+\.\d+$', to_ip):
            #     continue
            key = (from_ip, to_ip)
            cache[key] = cache.get(key, 0) + int(float(result['_count']))
        

    def scrape(self, start_time, end_time):
        volumes = {}
        warnings = {}
        errors = {}
    
        # Spaghetti
        good_query = self.get_good_query_in()
        warning_query = self.get_warning_query_in()
        bad_query = self.get_bad_query_in()
        
        self.__process_in(good_query, volumes, start_time, end_time)
        self.__process_in(warning_query, warnings, start_time, end_time)
        self.__process_in(bad_query, errors, start_time, end_time)
        
        good_query = self.get_good_query_out()
        warning_query = self.get_warning_query_out()
        bad_query = self.get_bad_query_out()
        self.__process_out(good_query, volumes, start_time, end_time)
        self.__process_out(warning_query, warnings, start_time, end_time)
        self.__process_out(bad_query, errors, start_time, end_time)

        # Convert sumologic results into edges
        edges = []
        for key in volumes.keys() + errors.keys() + warnings.keys():
            from_ip, to_ip = key
            volume = volumes.get(key, 0)
            error_volume = errors.get(key, 0)
            warning_volume = warnings.get(key, 0)
            edge = Edge(from_ip, to_ip, volume, warning_volume, error_volume)
            edges.append(edge)
        
        # from pprint import pprint
        # pprint([
        #     (edge.from_ip, edge.to_ip) for edge in edges
        # ])
        return self.post_process(edges)
    
    def get_good_query_in(self):
        pass

    def get_warning_query_in(self):
        pass
    
    def get_bad_query_in(self):
        pass
    
    def get_good_query_out(self):
        pass

    def get_warning_query_out(self):
        pass
    
    def get_bad_query_out(self):
        pass

    def post_process(self, edges):
        return edges
