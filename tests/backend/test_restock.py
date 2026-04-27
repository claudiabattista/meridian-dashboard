"""
Tests for the restock recommendations API endpoint.
"""
import pytest


class TestRestockRecommendations:
    """Test suite for /api/restock/recommendations endpoint."""

    def test_returns_200(self, client):
        """Endpoint returns HTTP 200."""
        response = client.get("/api/restock/recommendations")
        assert response.status_code == 200

    def test_returns_list(self, client):
        """Response is a list."""
        response = client.get("/api/restock/recommendations")
        assert isinstance(response.json(), list)

    def test_recommendation_fields(self, client):
        """Each recommendation has all required fields."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        required_fields = [
            "sku", "name", "category", "warehouse",
            "current_stock", "days_of_stock", "forecasted_demand",
            "recommended_quantity", "unit_cost", "total_cost", "urgency"
        ]

        for rec in data:
            for field in required_fields:
                assert field in rec, f"Missing field: {field}"

    def test_only_low_stock_items_returned(self, client):
        """Only items with fewer than 30 days of stock are recommended."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            assert rec["days_of_stock"] < 30, (
                f"{rec['sku']} has {rec['days_of_stock']} days of stock but was recommended"
            )

    def test_sorted_by_urgency(self, client):
        """Results are sorted most urgent first (lowest days_of_stock)."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        days = [rec["days_of_stock"] for rec in data]
        assert days == sorted(days), "Results are not sorted by days_of_stock ascending"

    def test_urgency_values_are_valid(self, client):
        """Urgency field is one of the three valid values."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        valid_urgencies = {"critical", "urgent", "low"}
        for rec in data:
            assert rec["urgency"] in valid_urgencies, f"Invalid urgency: {rec['urgency']}"

    def test_urgency_critical_threshold(self, client):
        """Items with < 7 days of stock are marked critical."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            if rec["days_of_stock"] < 7:
                assert rec["urgency"] == "critical", (
                    f"{rec['sku']} has {rec['days_of_stock']}d but urgency={rec['urgency']}"
                )

    def test_urgency_urgent_threshold(self, client):
        """Items with 7–14 days of stock are marked urgent."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            if 7 <= rec["days_of_stock"] < 14:
                assert rec["urgency"] == "urgent"

    def test_urgency_low_threshold(self, client):
        """Items with 14–30 days of stock are marked low."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            if 14 <= rec["days_of_stock"] < 30:
                assert rec["urgency"] == "low"

    def test_recommended_quantity_positive(self, client):
        """Recommended quantity is always at least 1."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            assert rec["recommended_quantity"] >= 1

    def test_total_cost_calculation(self, client):
        """total_cost equals recommended_quantity × unit_cost."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            expected = round(rec["recommended_quantity"] * rec["unit_cost"], 2)
            assert abs(rec["total_cost"] - expected) < 0.01, (
                f"{rec['sku']}: total_cost {rec['total_cost']} != {expected}"
            )

    def test_budget_cap_respected(self, client):
        """With a budget, total spend does not exceed the cap."""
        budget = 5000.0
        response = client.get(f"/api/restock/recommendations?budget={budget}")
        assert response.status_code == 200

        data = response.json()
        total = sum(rec["total_cost"] for rec in data)
        assert total <= budget + 0.01, f"Total {total} exceeds budget {budget}"

    def test_budget_cap_filters_items(self, client):
        """A very small budget returns fewer items than no budget."""
        no_budget = client.get("/api/restock/recommendations").json()
        small_budget = client.get("/api/restock/recommendations?budget=1").json()

        assert len(small_budget) <= len(no_budget)

    def test_zero_budget_ignored(self, client):
        """Budget of 0 is treated as no cap."""
        no_budget = client.get("/api/restock/recommendations").json()
        zero_budget = client.get("/api/restock/recommendations?budget=0").json()

        assert len(zero_budget) == len(no_budget)

    def test_large_budget_returns_all(self, client):
        """A very large budget returns all recommendations."""
        no_budget = client.get("/api/restock/recommendations").json()
        big_budget = client.get("/api/restock/recommendations?budget=9999999").json()

        assert len(big_budget) == len(no_budget)

    def test_numeric_field_types(self, client):
        """Numeric fields have correct types."""
        response = client.get("/api/restock/recommendations")
        data = response.json()

        for rec in data:
            assert isinstance(rec["current_stock"], int)
            assert isinstance(rec["days_of_stock"], (int, float))
            assert isinstance(rec["forecasted_demand"], int)
            assert isinstance(rec["recommended_quantity"], int)
            assert isinstance(rec["unit_cost"], (int, float))
            assert isinstance(rec["total_cost"], (int, float))
