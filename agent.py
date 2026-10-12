"""
The FitFindr planning loop.

Unit 4 adds:
- search_listings through MCP
- trace steps for every tool call
- ModelUnavailable handling
"""

import re

import config
import trace

from tools import (
    suggest_outfit,
    create_fit_card,
    compare_prices,
)

from mcp_client import call_tool
from generate import ModelUnavailable


# ── session state ──────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "price_comparison": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── planning loop ──────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:

    # Start a fresh trace for every run
    trace.start_trace()

    session = new_session(query, wardrobe)

    # ------------------------------------------------------------------
    # Parse query
    # ------------------------------------------------------------------

    max_price = None
    size = None

    price_match = re.search(
        r"(?:under|below|up to|max(?:imum)?)\s*\$?\s*(\d+(?:\.\d+)?)",
        query,
        flags=re.IGNORECASE,
    )

    if price_match:
        max_price = float(price_match.group(1))

    size_match = re.search(
        r"\bsize\s+([A-Za-z0-9/.+-]+)",
        query,
        flags=re.IGNORECASE,
    )

    if size_match:
        size = size_match.group(1)

    description = query

    if price_match:
        description = (
            description[:price_match.start()]
            + " "
            + description[price_match.end():]
        )

    description = re.sub(
        r"\bsize\s+[A-Za-z0-9/.+-]+",
        " ",
        description,
        flags=re.IGNORECASE,
    )

    description = re.sub(
        r"\b(?:looking\s+for|i\s+want|i'm\s+looking\s+for|find\s+me)\b",
        " ",
        description,
        flags=re.IGNORECASE,
    )

    description = re.sub(r",+", " ", description)
    description = re.sub(r"\s+", " ", description).strip()

    description = re.sub(
        r"^(?:a|an)\s+",
        "",
        description,
        flags=re.IGNORECASE,
    )

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    # ------------------------------------------------------------------
    # Planning loop
    # ------------------------------------------------------------------

    step = "search"
    iteration_count = 0

    while step != "done":

        iteration_count += 1
        trace.check_iterations(iteration_count)

        # ==============================================================
        # STEP 1 — Search through MCP
        # ==============================================================
        if step == "search":

            search_inputs = {
                "description": session["parsed"]["description"],
                "size": session["parsed"]["size"],
                "max_price": session["parsed"]["max_price"],
            }

            session["search_results"] = call_tool(
                "search_listings",
                search_inputs,
            )

            # Required empty-search branch
            if not session["search_results"]:

                session["error"] = (
                    "I couldn't find a matching item. Try increasing your "
                    "maximum price, changing the size, or using broader "
                    "search terms."
                )

                trace.step(
                    "search_listings (via MCP)",
                    inputs=search_inputs,
                    returned=session["search_results"],
                    note="branch: empty search, stopping",
                )

                return session

            trace.step(
                "search_listings (via MCP)",
                inputs=search_inputs,
                returned=session["search_results"],
            )

            session["selected_item"] = session["search_results"][0]

            step = "price_comparison"
            continue

        # ==============================================================
        # STRETCH TOOL — Compare prices
        # ==============================================================
        if step == "price_comparison":

            compare_inputs = {
                "selected_item": session["selected_item"],
                "search_results": session["search_results"],
            }

            session["price_comparison"] = compare_prices(
                session["selected_item"],
                session["search_results"],
            )

            trace.step(
                "compare_prices",
                inputs=compare_inputs,
                returned=session["price_comparison"],
            )

            step = "outfit"
            continue

        # ==============================================================
        # STEP 2 — Suggest outfit
        # ==============================================================
        if step == "outfit":

            outfit_inputs = {
                "new_item": session["selected_item"],
                "wardrobe": session["wardrobe"],
            }

            try:
                session["outfit_suggestion"] = suggest_outfit(
                    session["selected_item"],
                    session["wardrobe"],
                )

            except ModelUnavailable as exc:

                session["error"] = (
                    "The styling model couldn't be reached. "
                    "Check your GEMINI_API_KEY and try again."
                )

                trace.step(
                    "suggest_outfit",
                    inputs=outfit_inputs,
                    returned=str(exc),
                    note="model unavailable, stopping",
                )

                return session

            trace.step(
                "suggest_outfit",
                inputs=outfit_inputs,
                returned=session["outfit_suggestion"],
            )

            step = "fit_card"
            continue

        # ==============================================================
        # STEP 3 — Create fit card
        # ==============================================================
        if step == "fit_card":

            fit_card_inputs = {
                "outfit": session["outfit_suggestion"],
                "new_item": session["selected_item"],
            }

            try:
                session["fit_card"] = create_fit_card(
                    session["outfit_suggestion"],
                    session["selected_item"],
                )

            except ModelUnavailable as exc:

                session["error"] = (
                    "The fit-card model couldn't be reached. "
                    "Check your GEMINI_API_KEY and try again."
                )

                trace.step(
                    "create_fit_card",
                    inputs=fit_card_inputs,
                    returned=str(exc),
                    note="model unavailable, stopping",
                )

                return session

            trace.step(
                "create_fit_card",
                inputs=fit_card_inputs,
                returned=session["fit_card"],
            )

            step = "done"

    return session


# ── running directly ──────────────────────────────────────────────────────────

def _show(session: dict) -> None:

    if session["error"]:
        print(f"  stopped: {session['error']}")
        return

    item = session["selected_item"] or {}

    print(
        f"  found:    {item.get('title')} — "
        f"${item.get('price')} on {item.get('platform')}"
    )

    print(f"  price:    {session['price_comparison']}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":

    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")

    _show(
        run_agent(
            query="looking for a vintage graphic tee under $30",
            wardrobe=get_example_wardrobe(),
        )
    )

    print("\n=== A query it can't ===")

    _show(
        run_agent(
            query="designer ballgown size XXS under $5",
            wardrobe=get_example_wardrobe(),
        )
    )