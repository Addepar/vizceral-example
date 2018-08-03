import json
import os

from hackathon.aliases import get_host_for_ip

def process_edges(edges):
    edge_dict = {}
    for idx, edge in enumerate(edges):
        # if idx % 10 == 0:
        #     print(idx, len(edges))
        edge['from_ip'] = get_host_for_ip(edge['from_ip'], edge)
        edge['to_ip'] = get_host_for_ip(edge['to_ip'], edge)
        key = (edge['from_ip'], edge['to_ip'])
        if key in edge_dict:
            old_edge = edge_dict[key]
            old_edge['good_volume'] += edge['good_volume']
            old_edge['warning_volume'] += edge['warning_volume']
            old_edge['bad_volume'] += edge['bad_volume']
        else:
            edge_dict[key] = edge
    return edge_dict.values()

def main():
    for directory in os.listdir('hackathon/data'):
        edges = []
        folder = os.path.join('hackathon/data', directory)
        for filename in os.listdir(folder):
            input_filename = os.path.join(folder, filename)
            with open(input_filename) as f:
                edges += json.loads(f.read())['edges']
        
        # Do processing again just in case we update alias logic
        edges = process_edges(edges)

        output_filename = os.path.join('src/data', directory + '.json').replace(':', '-')
        # output_filename = os.path.join('hackathon/transformed', 'output.json').replace(':', '-')
        
        output = {
            "renderer": "global",
            "name": "edge",
            "nodes": [
                {
                    "renderer": "region",
                    "name": "us-west-1",
                    "maxVolume": 1000,
                    "class": "normal",
                    "updated": 1,
                    "nodes": [
                    ],
                    "connections": [
                    ]
                }
            ],
            "connections": []
        }
        nodes = set()
        for edge in edges:
            if edge['from_ip'] == '127.0.0.1' or edge['to_ip'] == '127.0.0.1':
                continue
            nodes.add(edge['from_ip'])
            nodes.add(edge['to_ip'])

            output['nodes'][0]['connections'].append({
                'source': edge['from_ip'],
                'target': edge['to_ip'],
                'metrics': {
                    'danger': edge['bad_volume'] / 3600.0,
                    'warning': edge['warning_volume'] / 3600.0,
                    'normal': edge['good_volume'] / 3600.0
                },
                'class': 'normal'
            })
        
        for node in nodes:
            output['nodes'][0]['nodes'].append({
                'name': node,
                'renderer': 'focusedChild',
                'class': 'normal'
            })
        with open(output_filename, 'w') as f:
            f.write(json.dumps(output))

if __name__ == '__main__':
    main()
