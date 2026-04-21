"""AI-generated unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


# KEPT: covers the edge case where max_item_id is 0 with no matching interactions
def test_filter_with_max_item_id_zero() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 0


# KEPT: covers multiple interactions all within the boundary
def test_filter_returns_multiple_interactions_within_max() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 1, 2), _make_log(3, 1, 3)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert len(result) == 3
    assert all(r.item_id <= 3 for r in result)


# DISCARDED: test duplicates test_filter_includes_interaction_at_boundary and adds no new value
# def test_boundary_value_exactly_equal() -> None:
#     interactions = [_make_log(1, 2, 5)]
#     result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
#     assert len(result) == 1


# KEPT: covers filter with single large max_item_id value
def test_filter_with_large_item_ids() -> None:
    interactions = [_make_log(1, 1, 100), _make_log(2, 1, 200)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=150)
    assert len(result) == 1
    assert result[0].item_id == 100


# KEPT: covers the scenario where all interactions exceed the max_item_id
def test_filter_excludes_all_interactions_above_max() -> None:
    interactions = [_make_log(1, 1, 10), _make_log(2, 1, 20)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert len(result) == 0
