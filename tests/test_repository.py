from sqlalchemy.sql import text
from src.dal.repo.repository import Repository
from src.domain.model import Batch, OrderLine

def insert_order_line(session):
      session.execute(text(
            "INSERT INTO order_lines (orderid, sku, qty)"
            "VALUES ('order_1', 'GENERIC-TABLE', 12)"
      ))
      [[orderline_id]] = session.execute(text(
            "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
            dict(orderid="order_1", sku="GENERIC-TABLE"))
      )
      return orderline_id

def insert_batch(session, batch_id):
       session.execute(text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES "
        '("batch1", "GENERIC-TABLE", 100, null)',
            dict(batch_id=batch_id)
        ))
       [[batch_id]] = session.execute(text(
             "SELECT id FROM batches WHERE reference=:batch_id AND sku='GENERIC-TABLE'",
             dict(batch_id=batch_id)
       ))
       return batch_id

def insert_allocations(session, orderline_id, batch_id):
      session.execute(text("INSERT INTO allocations (orerline_id, batch_id)"
                           "VALUES (:orderline_id, :batch_id)", 
                           dict(orderline_id=orderline_id, batch_id=batch_id)
                        ))

def test_repository_can_save_batch(session):
      pass
      # batch = Batch(ref="batch1", sku="GENERIC-TABLE", qty=100, eta=None)
      # print(f"object instance: {batch}")
      # repo = Repository(session)
      # repo.add(batch)
      # session.commit()

      # rows = session.execute(text(
      #       "SELECT reference, sku, _purchased_quantity, eta FROM 'batches'"
      # ))
      # assert list(rows) == [("batch1", "GENERIC-TABLE", 100, None)]

def test_repository_can_retrieve_batch_with_allocations(session):
      orderline_id = insert_order_line(session)
      batch1_id = insert_batch(session, "batch1")
      insert_batch(session, "batch1")
      insert_allocations(session, orderline_id, batch1_id)
      repo = Repository(session)
      retrieved = repo.get("batch1")
      expected = Batch("batch1", "GENERIC-TABLE", 100, eta=None)
      assert retrieved == expected