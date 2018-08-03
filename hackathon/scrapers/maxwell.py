from hackathon.scrapers.base import BaseScraper
from hackathon.aliases import ALIASES
from hackathon.models import Edge
class MaxwellScraper(BaseScraper):
    def get_good_query_out(self):
        # Use kafka as dest ip
        return '_sourceHost=maxwell.prod.addepar.com AND "Successfully published" | "10.0.2.225" as ip | count by _sourceHost, ip'
    def post_process(self, edges):
        if len(edges) > 1:
            raise RuntimeError('wut')
        elif not edges:
            return edges
        MAXWELL_CLIENTS = [
            alias for alias in ALIASES.keys() if (
                'prodcomp' in alias or 
                'snap' in alias or 
                'tx' in alias or
                'taxlot' in alias
            )
        ]
        for client in MAXWELL_CLIENTS:
            edges.append(Edge('kafka', client, edges[0].good_volume, 0, 0))
        return edges
