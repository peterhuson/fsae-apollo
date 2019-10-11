from abc import ABC, abstractmethod


# General class data readers should implement
class DataReader(ABC):
    @abstractmethod
    def get_data(self):
        ...


# Data reader that reads from the incoming serial connection from MoTeC
class SerialDataReader(DataReader):
    ...


# Stub data reader to provide dummy data when real data not available
class StubDataReader(DataReader):
    ...