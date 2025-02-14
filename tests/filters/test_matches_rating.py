import pytest

from lily.filters.matches_rating import satisfies_all_constraints, satisfies_constraint


class TestSatisfiesConstraints:
    def test_simple_constraints(self):
        assert satisfies_constraint(50, "> 0") is True
        assert satisfies_constraint(85, ">= 80") is True
        assert satisfies_constraint(75, "< 80") is True
        assert satisfies_constraint(80, "== 80") is True

        assert satisfies_constraint(80, "!= 80") is False

    def test_boundary_conditions(self):
        assert satisfies_constraint(80, ">= 80") is True  # Exact boundary
        assert satisfies_constraint(80, "<= 80") is True  # Exact boundary
        assert satisfies_constraint(79.99, "< 80") is True
        assert satisfies_constraint(80.01, "> 80") is True

    def test_negative_numbers(self):
        assert satisfies_constraint(-10, "< 0") is True
        assert satisfies_constraint(-1, "< 0") is True
        assert satisfies_constraint(-5, ">= -10") is True
        assert satisfies_constraint(-100, ">= -99") is False

    def test_float_comparisons(self):
        assert satisfies_constraint(3.5, "> 3.4") is True
        assert satisfies_constraint(3.5, "<= 3.5") is True
        assert satisfies_constraint(2.999, ">= 3") is False
        assert satisfies_constraint(3.14159, "== 3.14159") is True

    def test_invalid_constraints(self):
        with pytest.raises(ValueError):
            satisfies_constraint(80, "=> 80")  # Invalid operator

        with pytest.raises(ValueError):
            satisfies_constraint(80, ">< 80")  # Invalid operator

        with pytest.raises(ValueError):
            satisfies_constraint(80, "80 >")  # Wrong format

        with pytest.raises(ValueError):
            satisfies_constraint(80, "invalid")  # Non-numeric

        with pytest.raises(ValueError):
            satisfies_constraint(80, "")  # Empty string

    def test_whitespace_variations(self):
        assert satisfies_constraint(80, "  >=   80  ") is True  # Handles extra spaces
        assert satisfies_constraint(50, "  >  40") is True
        assert satisfies_constraint(10, "<=   10") is True


class TestSatisfiesAllConstraints:
    def test_satisfies_all_constraints(self):
        # Single constraint cases (delegates to satisfies_constraint)
        assert satisfies_all_constraints(50, "> 0") is True
        assert satisfies_all_constraints(85, ">= 80") is True
        assert satisfies_all_constraints(75, "< 80") is True
        assert satisfies_all_constraints(80, "== 80") is True
        assert satisfies_all_constraints(80, "!= 80") is False

    def test_multiple_constraints(self):
        # All constraints must be satisfied
        assert satisfies_all_constraints(50, "> 0, < 100") is True
        assert satisfies_all_constraints(85, ">= 80, < 90") is True
        assert satisfies_all_constraints(75, "< 80, >= 70") is True
        assert satisfies_all_constraints(80, "== 80, >= 50, < 100") is True

        # One constraint fails
        assert satisfies_all_constraints(80, "== 80, < 50") is False
        assert satisfies_all_constraints(60, ">= 50, <= 55") is False

    def test_whitespace_handling(self):
        # Constraints with extra spaces should still work
        assert satisfies_all_constraints(50, "  > 0 ,   < 100  ") is True
        assert satisfies_all_constraints(80, "  == 80  ,  >= 50  ,   < 100 ") is True

    def test_negative_numbers(self):
        assert satisfies_all_constraints(-10, "< 0, >= -20") is True
        assert satisfies_all_constraints(-5, ">= -10, < 0") is True
        assert satisfies_all_constraints(-50, ">= -40, < 0") is False  # Fails >= -40

    def test_float_values(self):
        assert satisfies_all_constraints(3.5, "> 3, < 4") is True
        assert satisfies_all_constraints(2.999, ">= 3, <= 3.5") is False  # Fails >= 3

    def test_invalid_constraints(self):
        # Malformed constraints should raise errors
        with pytest.raises(ValueError):
            satisfies_all_constraints(80, "=> 80")  # Invalid operator

        with pytest.raises(ValueError):
            satisfies_all_constraints(80, ">< 80")  # Invalid operator

        with pytest.raises(ValueError):
            satisfies_all_constraints(80, "80 >")  # Wrong format

        with pytest.raises(ValueError):
            satisfies_all_constraints(80, "invalid")  # Non-numeric

        with pytest.raises(ValueError):
            satisfies_all_constraints(80, "")  # Empty string

    def test_edge_cases(self):
        assert satisfies_all_constraints(80, ">= 80, <= 80") is True  # Exactly at boundary
        assert satisfies_all_constraints(80, "> 79, < 81") is True
        assert satisfies_all_constraints(80, "<= 79, >= 81") is False  # Impossible condition
