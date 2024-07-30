
import math
from constants import GENE_LENGTH

class PopulationStats:
    def __init__(self):
        self.gene_stats = {i: {'sum': 0, 'sum_sq': 0, 'count': 0} for i in range(GENE_LENGTH)}

    def add_creature(self, creature):
        for i, value in enumerate(creature.genes.values):
            self.gene_stats[i]['sum'] += value
            self.gene_stats[i]['sum_sq'] += value ** 2
            self.gene_stats[i]['count'] += 1

    def calculate_cv(self):
        cv = {}
        for i in range(GENE_LENGTH):
            stats = self.gene_stats[i]
            if stats['count'] > 0:
                mean = stats['sum'] / stats['count']
                variance = (stats['sum_sq'] / stats['count']) - (mean ** 2)
                std_dev = math.sqrt(max(0, variance))
                cv[i] = (std_dev / mean) if mean != 0 else 0
            else:
                cv[i] = 0
        return cv

    def reset(self):
        for stats in self.gene_stats.values():
            stats['sum'] = 0
            stats['sum_sq'] = 0
            stats['count'] = 0