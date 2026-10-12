"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each scenario below corresponds directly to one criterion in criteria.md.

run_eval.py will run every scenario five times.
"""

SCENARIOS = [
    {
        # Criterion 1:
        # A matching query should complete the full agent flow
        # and return a fit card.
        "name": "matching query completes full flow",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },

    {
        # Criterion 2:
        # An impossible query should stop immediately after search.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },

    {
        # Criterion 3:
        # A successful normal query lets us verify that the selected
        # listing is preserved through session state.
        "name": "selected item preserved in session",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 3,
    },

    {
        # Criterion 4:
        # Run the same successful item repeatedly so we can check whether
        # the fit card includes the selected item and a styling detail.
        "name": "fit card includes item and styling detail",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },

    {
        # Criterion 5:
        # Every returned listing must respect the requested max price.
        "name": "search respects max price",
        "query": "graphic tee under $20",
        "wardrobe": "example",
        "criterion": 5,
    },
]


WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed before starting a long evaluation."""
    problems = []

    for i, scenario in enumerate(SCENARIOS, 1):

        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")

        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )

        criterion = scenario.get("criterion")

        if criterion not in (1, 2, 3, 4, 5):
            problems.append(
                f"scenario {i} has invalid criterion {criterion!r}"
            )

    return problems