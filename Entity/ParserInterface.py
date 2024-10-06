from abc import ABC, abstractmethod

class ParserInterface(ABC):

    @abstractmethod
    def parse_data(self, data:str) -> dict:
        return NotImplementedError("This method should be implemented in subclasses")