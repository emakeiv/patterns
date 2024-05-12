from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey
import domain.model as model


metadata = Metadata()

order_lines = Table(
      'order_lines', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('sku', String(255)),
        Column('qty', Integer, nullable=False),
        Column('orderid', String(255)),
)

def start_mappers():
      line_mapper = mapper(model.OrderLine, order_lines)
