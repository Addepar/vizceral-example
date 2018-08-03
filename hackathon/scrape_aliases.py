from hackathon.aliases import ALIASES
from pluto.sumologic.sumo_search import SumoSearch

from datetime import datetime, timedelta
from pprint import pprint

def main():
    sumo = SumoSearch()
    start = datetime(2018, 7, 5, 20)
    end = start + timedelta(hours=1)
    results = sumo.search_job('_sourceHost=prod* | where !isEmpty(ip) | parse regex "firmid=(?<firm>\d+)" | split ip delim=\',\' extract ip, _ | where !(ip matches "10.*") AND ip matches "*.*.*.*" | count by ip, firm | sort by ip', start, end)
    
    ip_firm_map = {}
    for result in results:
        firm = result['firm']
        ip = result['ip']
        ip_firm_map[ip] = ip_firm_map.get(ip, []) + [firm]
    
    for ip, firms in ip_firm_map.items():
        # Support portal
        if '57' in firms:
            firms.remove('57')
        name = 'Firm ' + ', '.join(sorted(firms))
        ALIASES[name] = ALIASES.get(name, []) + [ip]
    
    results = sumo.search_job('_sourceHost=iverson* AND "Amazon Route 53" | parse regex "iverson: (?<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" | count by ip', start, end)
    for result in results:
        ALIASES['Amazon'] = list(set(ALIASES.get('Amazon', []) + [result['ip']]))
    
    pprint(ALIASES)

if __name__ == '__main__':
    main()
