import abc


class DataLoader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def data_is_loaded(self):
        pass

    @abc.abstractmethod
    def load_data(self):
        pass
