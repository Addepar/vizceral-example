import dateutil.parser

class Node:
    def __init__(self, ip, description):
        self.__ip = ip
        self.__description = description

    def to_dict(self):
        return {
            'ip': self.__ip,
            'description': self.__description
        }

    @staticmethod
    def from_dict(json):
        return Node(json['ip'], json['description'])

class Edge:
    def __init__(self, from_ip, to_ip, good_volume, warning_volume, bad_volume):
        self.from_ip = from_ip
        self.to_ip = to_ip
        self.good_volume = good_volume
        self.warning_volume = warning_volume
        self.bad_volume = bad_volume
    
    def to_dict(self):
        return {
            'from_ip': self.from_ip,
            'to_ip': self.to_ip,
            'good_volume': self.good_volume,
            'warning_volume': self.warning_volume,
            'bad_volume': self.bad_volume
        }
    
    @staticmethod
    def from_dict(json):
        return Edge(json['from_ip'], json['to_ip'], json['good_volume'], json['warning_volume'], json['bad_volume'])

class TimeSlice:
    def __init__(self, timestamp):
        self.__timestamp = timestamp
        self.edges = []

    @staticmethod
    def from_dict(json):
        timeslice = TimeSlice(dateutil.parser.parse(json['timestamp']))
        timeslice.edges = [
            Edge.from_dict(edge_json) for edge_json in json['edges']
        ]
        return timeslice

    def to_dict(self):
        return {
            'timestamp': self.__timestamp.isoformat(),
            'edges': [edge.to_dict() for edge in self.edges]
        }
