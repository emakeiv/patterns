from abc import ABC, abstractmethod
from src.domain.model import Batch

class IRepository(ABC):

      @abstractmethod
      def add(self, batch: Batch):
           raise NotImplementedError

      @abstractmethod
      def get(self, reference) -> Batch:
           raise NotImplementedError