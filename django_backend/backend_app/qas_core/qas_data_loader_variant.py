from abc import ABC, abstractmethod
import abc


class QASDataLoaderVariant(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_data(self, source_path='', output_path=''):
        pass

