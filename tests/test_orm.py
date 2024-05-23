import src.domain.model as model 
from datetime import date, timedelta
from sqlalchemy.sql import text

def test_orderline_mapper_can_load_lines(session):
    session.execute(text(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)')
    )
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected



def test_orderline_mapper_can_save_lines(session):
      new_line = model.OrderLine("order1", "FUNKY-TABLE", 10)
      session.add(new_line)
      session.commit()

      rows = list(session.execute(text("SELECT orderid, sku, qty FROM order_lines")))
      assert rows == [("order1", "FUNKY-TABLE", 10)]
   
def test_can_retrieve_batches(session):
    session.execute(text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES "
        '("batch1", "RED-CHAIR", 100, null),'
        '("batch2", "RED-TABLE", 200, "2020-03-02"),'
        '("batch3", "BLUE-LIPSTICK", 300, "2020-03-03")'
    ))
    expected = [
         model.Batch("batch1", "RED-CHAIR", 100, eta=None),
         model.Batch("batch2", "RED-TABLE", 200, eta=date(2020, 3, 2)),
         model.Batch("batch3", "BLUE-LIPSTICK", 300, eta=date(2020, 3, 3))
    ]

    assert session.query(model.Batch).all() == expected