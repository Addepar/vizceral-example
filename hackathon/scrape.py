import json
import os

from dateutil import rrule
from datetime import datetime, timedelta
from hackathon.models import TimeSlice
from hackathon.scrapers.http import HttpScraper
from hackathon.scrapers.repgen import RepgenScraper
from hackathon.scrapers.comp_worker import CompWorkerScraper
from hackathon.scrapers.snapshots import SnapshotScraper
from hackathon.scrapers.taxlots import TaxlotScraper
from hackathon.scrapers.transactions import TransactionScraper
from hackathon.scrapers.maxwell import MaxwellScraper
from hackathon.scrapers.nginx import NginxScraper
from hackathon.scrapers.adp import AdpScraper
from hackathon.scrapers.batu import BatuScraper
from hackathon.scrapers.adia import AdiaScraper
from hackathon.scrapers.wavefront import WavefrontScraper
from hackathon.aliases import get_host_for_ip
import hackathon.transformer as transformer

SCRAPERS = {
    'ApiLB': NginxScraper('_sourceHost=mslb-*-prod.addepar.com'),
    'Repgen': RepgenScraper(),
    'Iverson': NginxScraper('_sourceHost=iverson6.addepar.com AND "/api"', include_egress=False),
    'CompWorker': CompWorkerScraper(),
    'Snapshots': SnapshotScraper(),
    'Taxlots': TaxlotScraper(),
    'Transactions': TransactionScraper(),
    'Maxwell': MaxwellScraper(),
    'ADP' : AdpScraper('_sourceHost=mario*.adp.addepar.com'), 
    'Batu' : BatuScraper('_sourcecategory=prod/batu sourceapplication=batu'),
    'Adia' : AdiaScraper('_sourceCategory=prod/adia sourceapplication=adiad'),
    'SMS' : WavefrontScraper('ts("com.google.common.cache.LocalLoadingCache.sms_data_history.size", instance=prodcomp*)')
}

def process_edges(edges):
    edge_dict = {}
    for edge in edges:
        edge.from_ip = get_host_for_ip(edge.from_ip, return_unknown=False)
        edge.to_ip = get_host_for_ip(edge.to_ip, return_unknown=False)
        key = (edge.from_ip, edge.to_ip)
        if key in edge_dict:
            old_edge = edge_dict[key]
            old_edge.good_volume += edge.good_volume
            old_edge.warning_volume += edge.warning_volume
            old_edge.bad_volume += edge.bad_volume
        else:
            edge_dict[key] = edge
    return edge_dict.values()

def main():
    end = datetime.now().replace(microsecond=0,second=0,minute=0) + timedelta(hours=-1)
    end = datetime(2018, 8, 3, 2)
    start = end + timedelta(hours=-23)

    timestamps = [timestamp for timestamp in rrule.rrule(rrule.HOURLY, dtstart=start, until=end)]
    for timestamp in reversed(timestamps):
        print(timestamp)
        start = timestamp
        end = timestamp + timedelta(hours=1)

        folder = 'hackathon/data/' + start.isoformat()
        if not os.path.exists(folder):
            os.makedirs(folder)

        for scraper_name, scraper in SCRAPERS.items():
            filename = folder + '/' + scraper_name + '.json'
            if os.path.isfile(filename):
                continue
       
            timeslice = TimeSlice(start)
            print(scraper_name)
            timeslice.edges = process_edges(scraper.scrape(start, end))
            with open(filename, 'w') as f:
                f.write(json.dumps(timeslice.to_dict()))
    transformer.main()


if __name__ == '__main__':
    main()
