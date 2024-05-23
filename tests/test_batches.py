from datetime import date, timedelta
from src.domain.model import Batch, OrderLine, allocate, OutOfStock
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_availabel_smaller_than_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 22)
    assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_sku_do_not_match():
    batch = Batch("batch-001", "TESTABLE-CHAIR", 100, eta=None)
    line = OrderLine("order-001", "EXPENSIVE-CHAIR", 10)
    batch.can_allocate(line) is False


def test_prefers_current_stock_batches_to_shipment():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("order-001", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest_batch = Batch("speedy-batch", "MINIMAL-SPOON", 100, eta=today)
    later_batch = Batch("normal-batch", "MINIMAL-SPOON", 100, eta=tomorrow)
    latest_batch = Batch("slow-batch", "MINIMAL-SPOON", 100, eta=later)

    line = OrderLine("order-001", "MINIMAL-SPOON", 10)

    allocate(line, [earliest_batch, later_batch, latest_batch])

    assert earliest_batch.available_quantity == 90
    assert later_batch.available_quantity == 100
    assert latest_batch.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGH-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGH-POSTER", 100, eta=tomorrow)
    line = OrderLine("order-001", "HIGH-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-FORK", 10, eta=today)
    allocate(OrderLine("order-001", "SMALL-FORK", 10), [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order-001", "SMALL-FORK", 1), [batch])
