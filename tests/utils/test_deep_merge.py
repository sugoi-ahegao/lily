from typing import Any

from lily.utils.deep_merge import deep_merge_dicts


def test_deep_merge_merges_in_place():
    dictA = {"filters": {"matches_organized_value": True}}
    dictB = {"filters": {"matches_organized_value": False}}

    deep_merge_dicts(dictA, dictB)

    expected = {"filters": {"matches_organized_value": False}}
    actual = dictA

    assert expected == actual


def test_deep_merge_populates_missing_keys():
    dictA = {"filters": {"matches_organized_value": True}}
    dictB: dict[Any, Any] = {}

    expected = {"filters": {"matches_organized_value": True}}
    actual = deep_merge_dicts(dictA, dictB)

    assert expected == actual


def test_deep_merge_populates_missing_nested_keys():
    dictA = {"field_settings": {"performers": {"separator": ", "}}}
    dictB = {"field_settings": {"performers": {"limit": 3}}}

    expected: dict[Any, Any] = {"field_settings": {"performers": {"separator": ", ", "limit": 3}}}
    actual = deep_merge_dicts(dictA, dictB)

    assert expected == actual


def test_deep_merge_does_not_override_set_values():
    dictA = {"filters": {"matches_organized_value": True}}
    dictB = {"filters": {"matches_organized_value": False}}

    expected = {"filters": {"matches_organized_value": False}}
    actual = deep_merge_dicts(dictA, dictB)

    assert expected == actual


def test_deep_merge_does_not_merge_lists():
    dictA = {"field_settings": {"performers": {"exclude_genders": ["MALE"]}}}
    dictB = {"field_settings": {"performers": {"exclude_genders": ["FEMALE"]}}}

    expected = {"field_settings": {"performers": {"exclude_genders": ["FEMALE"]}}}
    actual = deep_merge_dicts(dictA, dictB)

    assert expected == actual
