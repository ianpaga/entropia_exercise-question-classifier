from abc import ABC, abstractmethod

class Question(ABC):
    @abstractmethod
    def ask(self):
        pass