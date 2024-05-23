from src.domain.model import OrderLine, Batch
from src.dal.repo.irepository import IRepository

class Repository(IRepository):

      def __init__(self, session) -> None:
            self.session = session

      def add(self, batch):
            self.session.add(batch)

      def get(self, reference):
            return self.session.query(Batch).filter_by(reference=reference).one()
      
      def list(self):
            return self.session.query(Batch).all()