# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is a thrift-shopping agent that helps a user search for an item based on description, size, and price. It searches available listings, selects the best matching item, and uses the user's existing wardrobe to suggest an outfit. It then creates a short social-media-style fit card. If no listing matches, the agent stops early and tells the user what they can change in their search.



---

## Tool Inventory


### search_listings

**What it does:** Searches the listings data using the requested description, optional size, and maximum price.

**Inputs:**
- `description` (`str`) — description of the item the user wants.
- `size` (`str` or `None`) — optional requested size.
- `max_price` (`float` or `None`) — optional maximum price.

**Returns:** A list of matching listing dictionaries containing fields such as title, price, size, platform, category, style tags, colors, and brand.

**When nothing matches:** Returns an empty list `[]`.

**Size matching:** Sizes are compared case-insensitively using tokens, so a requested `M` can match `S/M` without using unsafe substring matching.

### suggest_outfit

**What it does:** Uses the selected new item and the user's wardrobe to suggest an outfit that goes with the item.

**Inputs:**
- `new_item` (`dict`) — the listing selected by the agent.
- `wardrobe` (`dict`) — a wardrobe dictionary containing an `items` list.

**Returns:** A `str` containing an outfit suggestion using the selected listing and wardrobe items.

**When the wardrobe is empty:** Returns a `str` containing general styling advice instead of failing.



### create_fit_card

**What it does:** Creates a short, post-ready caption describing the selected item and suggested outfit.

**Inputs:**
- `outfit` (`str`) — the outfit suggestion.
- `new_item` (`dict`) — the selected listing.

**Returns:** A `str` containing a short, post-ready fit-card caption.

**When the outfit is empty:** If `outfit` is empty or whitespace, returns a descriptive `str` explaining that a fit card could not be created instead of crashing.

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, the agent stores a useful message in the session and stops. It does not call `suggest_outfit` or `create_fit_card`. Otherwise, it selects the first listing, stores it in the session, and continues to `suggest_outfit`.



**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** The agent uses regular expressions to extract the optional size and maximum price from the user's query. The remaining text is cleaned and used as the search description.

**What moves through the session:** The parsed query is stored in `session["parsed"]`, search results go into `session["search_results"]`, the first result is stored in `session["selected_item"]`, the outfit is stored in `session["outfit_suggestion"]`, and the final caption is stored in `session["fit_card"]`.

---

## Sample Run

**One full query**

```text
$ python agent.py

=== A query the data can match ===
found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

outfit: Here are two ways to style your new Y2K baby tee using pieces from your wardrobe:

Outfit 1: Sweet & Edgy Streetwear
- Y2K Baby Tee — Butterfly Print
- Baggy straight-leg jeans
- Vintage black denim jacket
- Chunky white sneakers
- Black crossbody bag

Outfit 2: Casual Contrast (Y2K Meets Earth Tones)
- Y2K Baby Tee — Butterfly Print
- Wide-leg khaki trousers
- Chunky white sneakers
- Brown leather belt
- Black crossbody bag

fit card: Channel major early 2000s energy with this Y2K butterfly print baby tee, available on depop now for just $18.0! Style it with baggy dark-wash jeans and a vintage denim jacket for the ultimate sweet-and-edgy streetwear fit. It's giving effortless retro cool-girl vibes all season long.

=== A query it can't ===
stopped: I couldn't find a matching item. Try increasing your maximum price, changing the size, or using broader search terms.
fit_card is None — it should still be None here

The second one should stop before the fit card. If both paths look the same,
the branch isn't doing anything yet.
```

**The three tools, tested one at a time**

```text
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

Returned matching listings including:
- Y2K Baby Tee — Butterfly Print — $18.0
- Graphic Tee — 2003 Tour Bootleg Style — $24.0
- Vintage Band Tee — Faded Grey — $19.0

All returned listings were at or below the $30 maximum price.
```

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit combinations using the vintage Levi's 501 jeans and pieces from your current wardrobe:

Outfit 1: Effortless Casual Streetwear
- White ribbed tank top
- Chunky white sneakers
- Brown leather belt
- Black crossbody bag

Outfit 2: Cozy Layered Grunge
- Oversized grey crewneck sweatshirt
- Vintage black denim jacket
- Black combat boots
```

```text
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats a classic pair of Vintage Levi's 501 Jeans in that perfect medium indigo wash. Grab these on Depop right now for just $38.0 to instantly nail that effortless streetwear vibe. Style them with crisp white sneakers for the ultimate off-duty look that goes with everything.
```

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->
**Moment 1**

- **What I asked for:** I asked AI to help implement `search_listings` while following the starter requirements for description, size, and maximum-price filtering.
- **What came back:** The suggested implementation tokenized listing text, filtered deterministic fields first, ranked results using keyword overlap, and returned an empty list when nothing matched.
- **What I changed:** I kept the starter function signature and data loader and used token-based size matching instead of a simple substring match to avoid incorrect size matches.

**Moment 2**

- **What I asked for:** I asked AI to help build the planning loop while keeping state visible in the session dictionary.
- **What came back:** The loop searched first, checked whether results were empty, stored the selected item in session state, then called the outfit and fit-card tools using values read back from the session.
- **What I changed:** I added a useful early-stop message telling the user to change the price, size, or search terms instead of returning only "No results."

## Stretch Feature — Fourth Tool

I added a fourth tool called `compare_prices`.

`compare_prices(selected_item, search_results)` compares the selected listing
with the other matching listings and returns a `str` explaining how the
selected item's price compares with the average price of the matching listings.

The agent calls this tool after selecting a listing and before generating the
outfit suggestion.

**Example run:**

```text
=== A query the data can match ===
found: Y2K Baby Tee — Butterfly Print — $18.0 on depop
price: Y2K Baby Tee — Butterfly Print costs $18.00, which is cheaper than the average matching-listing price of $21.30.
outfit: Here are two ways to style your new Y2K baby tee using pieces from your wardrobe:
fit card: Channel major early 2000s energy with this Y2K butterfly print baby tee, available on depop now for just $18.0!

=== A query it can't ===
stopped: I couldn't find a matching item. Try increasing your maximum price, changing the size, or using broader search terms.
fit_card is None — it should still be None here

<!-- ═══════════════════════ UNIT 4 — THE TEST ═════════════════
══════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
