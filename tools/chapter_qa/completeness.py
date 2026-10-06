"""Expected versus observed inventory. Empty input is not a clean pass."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryCount:
    name: str
    expected: int | None
    observed: int | None
    explicitEmptyAllowed: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "expected": self.expected,
            "observed": self.observed,
            "explicitEmptyAllowed": self.explicitEmptyAllowed,
        }


def assess_completeness(expected_inputs, observed_inputs, inventory) -> list[str]:
    """Return failure codes. An empty code list means the inventory may proceed.

    Zero declared inputs are not zero defects. A matching positive count may proceed.
    An explicit empty inventory is accepted only when that count sets explicitEmptyAllowed.
    """
    codes = []
    expected_inputs = [str(item).strip() for item in (expected_inputs or []) if str(item).strip()]
    observed_inputs = [str(item).strip() for item in (observed_inputs or []) if str(item).strip()]
    inventory = list(inventory or [])

    if not expected_inputs:
        codes.append("ZERO_INPUT")
    missing = [item for item in expected_inputs if item not in observed_inputs]
    if expected_inputs and missing:
        codes.append("MISSING_INPUT")
    if not inventory:
        codes.append("INCOMPLETE_INVENTORY")

    for item in inventory:
        name = item.name if isinstance(item, InventoryCount) else item["name"]
        if not str(name or "").strip():
            codes.append("INCOMPLETE_INVENTORY")
            continue
        expected = item.expected if isinstance(item, InventoryCount) else item.get("expected")
        observed = item.observed if isinstance(item, InventoryCount) else item.get("observed")
        explicit = (
            item.explicitEmptyAllowed
            if isinstance(item, InventoryCount)
            else bool(item.get("explicitEmptyAllowed", False))
        )
        if expected is None or observed is None:
            codes.append("INCOMPLETE_INVENTORY")
            continue
        if expected == 0 and observed == 0:
            if not explicit:
                codes.append("ZERO_INPUT")
            continue
        if expected == 0 or observed == 0:
            codes.append("ZERO_INPUT")
            continue
        if expected != observed:
            codes.append("COUNT_MISMATCH")
            continue
        if not name:
            codes.append("INCOMPLETE_INVENTORY")
    return codes
