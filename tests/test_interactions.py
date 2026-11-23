
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_product_interactions.csv"
)


@pytest.fixture(scope="module")
def interactions():
    """Load customer-product interaction data."""

    assert DATA_PATH.exists(), (
        f"Interaction dataset not found: {DATA_PATH}"
    )

    df = pd.read_csv(DATA_PATH)

    assert not df.empty, "Interaction dataset is empty"

    return df


def test_required_columns_exist(interactions):
    required_columns = {
        "CustomerID",
        "StockCode",
        "PurchaseCount",
        "TotalQuantity",
        "TotalSpend",
        "InteractionStrength"
    }

    assert required_columns.issubset(set(interactions.columns))


def test_customer_ids_are_not_missing(interactions):
    assert interactions["CustomerID"].notna().all()


def test_product_ids_are_not_missing(interactions):
    assert interactions["StockCode"].notna().all()


def test_purchase_counts_are_positive(interactions):
    assert (interactions["PurchaseCount"] > 0).all()


def test_total_quantities_are_positive(interactions):
    assert (interactions["TotalQuantity"] > 0).all()


def test_total_spending_is_positive(interactions):
    assert (interactions["TotalSpend"] > 0).all()


def test_interaction_strength_is_valid(interactions):
    expected_strength = np.log1p(interactions["PurchaseCount"])

    assert np.isfinite(interactions["InteractionStrength"]).all()

    assert np.allclose(
        interactions["InteractionStrength"],
        expected_strength,
        rtol=1e-5,
        atol=1e-6
    )


def test_customer_product_pairs_are_unique(interactions):
    duplicate_pairs = interactions.duplicated(
        subset=["CustomerID", "StockCode"]
    )

    assert not duplicate_pairs.any()


def test_interaction_dataset_has_expected_records(interactions):
    assert len(interactions) == 266110
