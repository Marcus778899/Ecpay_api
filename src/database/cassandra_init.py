import os
import logging
from pathlib import Path
from cassandra.cluster import Cluster,DCAwareRoundRobinPolicy

class CassadnraDB:
    def __init__(self):
        self.ip = []
        with open(os.path.join(Path(__file__).parent,'setting.txt'),"r") as file:
            for line in file:
                self.ip.append(line.strip())
        self.cluster = Cluster(
            contact_points=self.ip,
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc = 'datacenter1'),
            protocol_version=4
            )
        try:
            self.session = self.cluster.connect('telegram')
            print(f"Cassandra connected")
        except Exception as e:
            logging.error(f"Cassandra connection error: {e}")

    def close_driver(self):
        self.session.shutdown()
        self.cluster.shutdown()
        print(f"Cassandra close")