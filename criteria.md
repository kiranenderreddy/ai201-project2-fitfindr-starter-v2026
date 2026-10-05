## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
required tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
The search step is deterministic, but `suggest_outfit` and `create_fit_card`
use a language model, so their output can vary between runs. A target of 4 out
of 5 allows for occasional model variability while still requiring the full
agent workflow to succeed consistently.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This branch depends only on whether `search_listings` returns an empty list and
does not depend on model output. Because the behavior is deterministic, it
should work correctly in every run.

---

## 3. The selected listing is preserved through session state

For 5 of 5 successful runs, the `id` stored in
`session["selected_item"]` is the same listing `id` passed to
`suggest_outfit`.

**Why this target:**
The agent uses session state to pass the selected search result to later tools.
Because this state transfer is deterministic, the same item should be preserved
in every successful run.

---

## 4. The fit card includes the selected item and a styling detail

For at least 4 of 5 successful runs, the fit card mentions the selected item
and includes at least one specific styling detail from the outfit suggestion.

**Why this target:**
`create_fit_card` uses a language model, so exact wording can vary between
runs. Requiring the selected item and a styling detail checks that the model is
using the information supplied by the previous tools without requiring
identical output every time.

---

## 5. Search respects the maximum-price filter

For 5 of 5 searches that include a `max_price`, every listing returned by
`search_listings` has a price less than or equal to the requested maximum.

**Why this target:**
The price ceiling is handled directly in deterministic Python filtering rather
than by the language model. A listing above the requested maximum would be a
search-tool bug, so this should pass in every run.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
