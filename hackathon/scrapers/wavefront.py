import wavefront_api_client as wave_api
import requests.packages.urllib3
import numpy as np
from datetime import datetime
from hackathon.models import Node, Edge
from pluto.config_reader import ConfigReader

config = ConfigReader('~/config/secrets.addepar')
requests.packages.urllib3.disable_warnings()

base_url = 'https://metrics.wavefront.com'
api_key = config.get_param('Wavefront', 'api_key')

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def unix_to_datetime(unix):
    return datetime.utcfromtimestamp(unix)#.strftime('%Y-%m-%d %H:%M:%S')

class WavefrontScraper(object):
    def __init__(self, query):
        '''
        query: str: WF query
        '''
        super(WavefrontScraper, self).__init__()
        config = wave_api.Configuration()
        config.host = base_url
        client = wave_api.ApiClient(configuration=config, header_name='Authorization', header_value='Bearer ' + api_key)
        self.query_api = wave_api.QueryApi(client)
        self.query = query
        # query by minute
        self.interval = 'm'

    def scrape(self, start, end):
        start_epoch = str(unix_time_millis(start))
        end_epoch = str(unix_time_millis(end))
        # print unix_to_datetime(float(start_epoch)/1000.0)
        # print unix_to_datetime(float(end_epoch)/1000.0)
        queries = self.query_api.query_api(self.query, start_epoch, self.interval, e=end_epoch)
        service_dict = dict((query_data.tags['instance'], WavefrontScraper.transform_wf_data(query_data.data)) for query_data in queries.timeseries)
        edges = []
        for service, timeseries in service_dict.iteritems():
            size_additions = []
            for i in range(1, len(timeseries)):
                prev_value = timeseries[i-1]
                value = timeseries[i]
                # to account for cache warming
                if value[1] > prev_value[1]:
                    size_additions.append(value[1] - prev_value[1])
            if len(size_additions) != 0:
                edges.append(Edge(service + '.prod.addepar.com', 'sms.addepar.com', np.mean(size_additions) * 60.0, 0, 0))
        return edges

    @staticmethod
    def transform_wf_data(data):
        return [[unix_to_datetime(long(datum[0])), datum[1]] for datum in data]

# q = 'ts("com.google.common.cache.LocalLoadingCache.sms_data_history.size", instance=prodcompa*)'
# s = "1533154914000"
# g = "m"

# wf = WavefrontScraper(q)
# start =datetime(2018, 8, 1, 21)
# end = datetime(2018, 8, 1, 22)
# wf.scrape(start, end)

