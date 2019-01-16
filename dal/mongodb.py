from . import *

class MongoDB:

    def __init__(self):
        self.periods = ["TTM", "TTM-1", "TTM-2", "TTM-3", "TTM-4",
                        "Q1", "Q2", "Q3", "Q4", "H1", "H2", "FY", "9M"]

    def save_metrics(self, metrics_names):
        for name in metrics_names:
            for period in self.periods:
                metric = Metric(name=name, period=period)
                metric.save()

