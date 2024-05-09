from datetime import date, timedelta
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    pytest.fail("TODO")

def test_can_allocate_if_available_greater_than_required():
    pytest.fail("TODO")

def test_cannot_allocate_if_availabel_smaller_than_required():
    pytest.fail("TODO")

def test_can_allocate_if_available_equal_to_required():
    pytest.fail("TODO")

def test_prefers_warehouse_batches_to_shipment():
    pytest.fail("TODO")

def test_prefers_earlier_batches():
    pytest.fail("TODO")