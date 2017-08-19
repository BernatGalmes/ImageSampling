import numpy as np
import scipy.stats as stats

class Stats:
    def __init__(self, data):
        self.data = data

    def confidence_interval(self, ic =0.99):
        return stats.t.interval(ic, len(self.data) - 1, loc=np.mean(self.data), scale=np.std(self.data))

    def mean(self):
        return np.mean(self.data)

    def std(self):
        return np.std(self.data)