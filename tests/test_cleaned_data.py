
from pathlib import Path

import pandas as pd
import pytest


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_retail.csv"


@pytest.fixture(scope="module")
def cleaned_data():
    """Load cleaned transaction data once for this test module."""

    assert DATA_PATH.exists(), f"Dataset not found: {DATA_PATH}"

    df = pd.read_csv(DATA_PATH)

    assert not df.empty, "Cleaned dataset is empty"

    return df


def test_required_columns_exist(cleaned_data):
    required_columns = {
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country"
    }

    assert required_columns.issubset(set(cleaned_data.columns))


def test_customer_ids_are_not_missing(cleaned_data):
    assert cleaned_data["CustomerID"].notna().all()


def test_quantities_are_positive(cleaned_data):
    assert (cleaned_data["Quantity"] > 0).all()


def test_unit_prices_are_positive(cleaned_data):
    assert (cleaned_data["UnitPrice"] > 0).all()


def test_cancelled_invoices_are_removed(cleaned_data):
    invoice_numbers = cleaned_data["InvoiceNo"].astype(str)

    assert not invoice_numbers.str.startswith("C").any()


def test_duplicate_transactions_are_removed(cleaned_data):
    assert not cleaned_data.duplicated().any()


def test_cleaned_dataset_has_expected_records(cleaned_data):
    assert len(cleaned_data) == 392692
