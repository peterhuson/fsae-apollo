from abc import ABC, abstractmethod
from typing import List, Dict, Any
from serial import Serial
from dataTransfer.dataProcessing import parse_data


# General class data readers should implement
class DataReader(ABC):
    @abstractmethod
    def get_data(self):
        ...


# Data reader that reads from the incoming serial connection from MoTeC
class SerialDataReader(DataReader):
    def __init__(self):
        self.serial_port = Serial("/dev/ttyAMA3", 115200, timeout=1)

    def get_raw_data(self) -> List[bytes]:
        return self.serial_port.readlines()

    def get_parsed_data(self) -> Dict[str, Any]:
        return parse_data(self.serial_port.readlines())

    def close(self) -> None:
        self.serial_port.close()


# Stub data reader to provide dummy data when real data not available
class StubDataReader(DataReader):
    def get_data(self):
        return self.values  # TODO: fix stub data
