from abc import ABC, abstractmethod

class ValuationModel(ABC):

    def __init__(self, simfin_id):
        self.company_id = simfin_id

    @abstractmethod
    def prepare_model_input(self):
        pass

    @abstractmethod
    def run(self):
        pass