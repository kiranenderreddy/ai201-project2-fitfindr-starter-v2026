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

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three required tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit and returns an actionable message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected listing is preserved through session state and passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the selected item and at least one specific styling detail from the outfit suggestion | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the requested maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

### Real output from one try

**Criterion 1 — `agent.py::run_agent` through `run_eval.py`**

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] compare_prices
      in:  dict with keys: selected_item, search_results
      out: Y2K Baby Tee — Butterfly Print costs $18.00, which is cheaper than the average matching-listing price of $21.3…
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two outfit combinations using your new Y2K baby tee...
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channel your inner 2000s icon with this adorable Y2K Butterfly Baby Tee...

try 1: completed — fit card 304 chars
```

**Criterion 2 — `agent.py::run_agent` empty-search branch**

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty search, stopping

try 1: stopped early — I couldn't find a matching item. Try increasing your maximum price, changing the size, or using broader search terms.
```

**Criterion 3 — `agent.py::run_agent` / `suggest_outfit` state verification**

```text
Try 1: selected_id=lst_002, passed_to_suggest_outfit=lst_002, PASS=True
Try 2: selected_id=lst_002, passed_to_suggest_outfit=lst_002, PASS=True
Try 3: selected_id=lst_002, passed_to_suggest_outfit=lst_002, PASS=True
Try 4: selected_id=lst_002, passed_to_suggest_outfit=lst_002, PASS=True
Try 5: selected_id=lst_002, passed_to_suggest_outfit=lst_002, PASS=True
```

**Criterion 4 — `tools.py::suggest_outfit` → `tools.py::create_fit_card`**

```text
Outfit suggestion:

Top (New): Y2K Baby Tee — Butterfly Print
Bottoms: Baggy straight-leg jeans, dark wash
Outerwear: Vintage black denim jacket
Shoes: Chunky white sneakers
Accessories: Black crossbody bag

Fit card:

Serving major early 2000s energy with this dreamy Y2K Butterfly Baby Tee!
Available on depop for just $18.0, I’m styling it with baggy dark-wash jeans
and chunky white sneakers for the ultimate retro streetwear contrast.
It’s the perfect blend of cute and effortless—grab it before it’s gone!
```

**Criterion 5 — `search_listings` through `mcp_client.call_tool`**

```text
[
  ('Y2K Baby Tee — Butterfly Print', 18.0),
  ('Mesh Long-Sleeve Top — Black', 15.0),
  ('Vintage Band Tee — Faded Grey', 19.0)
]

ALL <= 20: True
```

The baseline evaluation was run with caching disabled using:

```text
python run_eval.py --label before
```

The complete evaluation evidence was saved to:

```text
results/run_2026-10-11_2046_before.md
```
## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three required tools and returns a fit card | 4 of 5 | MET (5/5) | All five runs successfully completed the MCP search, outfit suggestion, and fit-card generation steps and returned a non-empty fit card. |
| 2 | Impossible query stops before suggest_outfit and returns an actionable message | 5 of 5 | MET (5/5) | All five impossible searches returned an empty result, stopped at the branch before suggest_outfit, and told the user to change the price, size, or search terms. |
| 3 | Selected listing is preserved through session state and passed to suggest_outfit | 5 of 5 | MET (5/5) | In all five checks, session selected_item had ID `lst_002` and the item passed into suggest_outfit also had ID `lst_002`. |
| 4 | Fit card includes the selected item and at least one specific styling detail from the outfit suggestion | 4 of 5 | MET (5/5) | Every fit card named the selected Y2K Butterfly Baby Tee and carried over at least one specific styling detail such as baggy dark-wash jeans, chunky white sneakers, or the vintage black denim jacket. |
| 5 | Search results respect the requested maximum price | 5 of 5 | MET (5/5) | The $20 search returned listings priced at $18, $15, and $19. No returned listing exceeded the requested maximum price. |

**Diagnoses**

No acceptance criteria were missed in the baseline evaluation. All five criteria met or exceeded their original targets.

The MCP search tool behaved consistently, including maximum-price filtering. The empty-search branch also behaved correctly and stopped the planning loop before downstream model tools were called. Session state preserved the selected listing correctly between steps, and the model-generated outfit suggestions and fit cards satisfied the content criterion in all five attempts.

The main weakness exposed by the evaluation is that Criteria 1, 3, and 4 use the same successful query and selected item repeatedly. This proves repeatability for that item, but it does not strongly test whether the same behavior holds for different clothing types or styling combinations.

Criterion 4 is also the most model-dependent criterion. It passed 5 of 5 times, but the fit-card generation depends on the model carrying a concrete styling detail from the outfit suggestion into the final card. That is the area I would strengthen first because a future model response could still produce a generic fit card even though the current five tries passed.



---

## Loop Trace

### Happy path

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more

[2] compare_prices
      in:  dict with keys: selected_item, search_results
      out: Y2K Baby Tee — Butterfly Print costs $18.00, which is cheaper than the average matching-listing price of $21.30...

[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two ways to style your new Y2K baby tee using pieces from your wardrobe...

[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channel major early 2000s energy with this Y2K butterfly print baby tee...
```

### Empty search

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty search, stopping

I couldn't find a matching item. Try increasing your maximum price,
changing the size, or using broader search terms.
```

### Failure-mode checks

- **Empty search:** The agent stopped after `search_listings` and told the user to change the price, size, or search terms.
- **Empty wardrobe:** The agent returned general styling advice and still created a fit card.
- **Model unavailable:** The agent reported that the model could not be reached and told the user to check `GEMINI_API_KEY` and try again.

### On the MCP move

`search_listings` was moved from a direct Python function call to an MCP tool call through `mcp_client.call_tool`. The search results and normal agent behavior remained the same; only the way the search tool is invoked changed.

---

## The Improvement

**What I changed:**

I made one targeted change to the `create_fit_card` prompt in `tools.py`.

Before:

```text
- Include at least one specific styling detail from the outfit suggestion.
```

After:

```text
- REQUIRED: Include at least one specific named wardrobe piece or concrete styling detail from the outfit suggestion; do not replace it with generic styling language.
```

I made only this one change before running the complete evaluation again.

**Which failure it was meant to fix:**

No acceptance criterion failed in the baseline evaluation. However, Criterion 4 was the most model-dependent part of the system. The fit-card generator could potentially satisfy the rest of the prompt while replacing the outfit recommendation with generic styling language.

The change was intended to reduce that model-output risk by explicitly requiring the generated fit card to carry at least one named wardrobe piece or concrete styling detail from the outfit suggestion.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three required tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit and returns an actionable message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected listing is preserved through session state and passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes the selected item and at least one specific styling detail from the outfit suggestion | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the requested maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**After-run Criterion 4 examples:**

```text
Try 1:
Fit card:
Channel total Y2K streetwear energy with this adorable Butterfly Print
Baby Tee... Style it with baggy straight-leg jeans in a dark wash and
chunky white sneakers...

Try 2:
Fit card:
Snagged this adorable Y2K Butterfly Baby Tee... I'm styling it with
baggy straight-leg jeans and chunky white sneakers...

Try 3:
Fit card:
Just scored this dreamy Y2K Butterfly Print Baby Tee... My favorite way
to style it is with baggy straight-leg jeans and chunky white sneakers...

Try 4:
Fit card:
Channel total 2000s energy with this dreamy Y2K Butterfly Baby Tee...
I styled it with baggy dark-wash straight-leg jeans...
Finish the look with chunky white sneakers...

Try 5:
Fit card:
Scored this adorable Y2K Butterfly Baby Tee... I can't wait to style it
with baggy straight-leg jeans and chunky white sneakers...
```

The full after-run evidence was saved to:

```text
results/run_2026-10-11_2102_after.md
```

**Did it help, and how do I know:**

The change did not increase the numerical pass rate because Criterion 4 had already passed 5 of 5 baseline tries. After the change, it again passed 5 of 5.

However, the after-run output shows that every fit card continued to include concrete styling information taken from the outfit suggestion, such as baggy straight-leg jeans, chunky white sneakers, a vintage black denim jacket, wide-leg khaki trousers, or a brown leather belt.

Therefore, there was no measurable improvement in the acceptance-criterion score because the baseline was already at the ceiling, but the prompt now expresses the requirement more explicitly and reduces the risk of future generic model responses.

---

## What's Still Broken

No acceptance criteria remain missed after the improvement. All five criteria were MET in both the before and after evaluations.

The evaluation is still limited in coverage. Several criteria repeatedly use the same `vintage graphic tee under $30` query, which consistently selects the same Y2K Butterfly Baby Tee. This demonstrates repeatability for that path but does not prove the same quality for every clothing category, price range, size, or wardrobe combination.

The outfit suggestion and fit-card tools also depend on model-generated output. Even with a stronger prompt, future responses can vary. A larger evaluation set containing different item categories and wardrobes would provide stronger evidence of reliability.

The MCP migration itself did not change the search behavior. `search_listings` now runs through `mcp_client.call_tool`, while filtering, selected-item behavior, and the empty-search branch continued to behave correctly in both evaluation runs.

I stopped after this single measured improvement because the assignment requires one diagnosis-driven change and a complete before/after evaluation. A useful next step would be to expand the scenarios to cover several different clothing categories and wardrobe combinations.