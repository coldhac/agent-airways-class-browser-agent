# Team 11 select seat

Team members: Mengyu Wu and Mingyu Gao.

`team_tools/select_seat.py` receives a seat-code dictionary, selects that one
visible, available seat, and returns the selection actually observed in the
browser. Success requires the exact selected button, the matching seat message,
and an enabled Continue button. It stays on the seat screen.

## Assignment and starting point

The Section 06 spreadsheet and companion 14-team Word assignment assign Team 11
`select_seat`, with `validate(argument)` and `run(page, argument, context)` in a
separate module under `team_tools/`. These specific instructions supersede the
older notebook's 17-team table and shared-file interface. The notebook's rubric,
independent-check requirement, and success/failure demonstrations still apply.

The public starter currently provides only `open_site` and `read_page`.
Its central validator and dispatcher still require string arguments. The
14-team integration notes reserve updating these for the TA, so this contribution
is tested directly without changing the common agent or the dropdown warm-up.
No language model, API key, or Ollama installation is needed for these tests.

## Interface and input checks

Example model proposal (documentation only; no model is called):

```json
{"action": "select_seat", "argument": {"seat": "1A"}}
```

`validate(argument)` returns `(bool, explanation)`. The only accepted key is
`seat`. Its value must be a positive row number followed by one uppercase letter,
with no surrounding spaces. Seat existence and availability are read from the
page rather than hardcoded in the validator. For example, `99Z` is well formed
but is rejected by `run` because no matching seat exists.

Given a Playwright page already on the seat screen, trusted Python can call:

```python
from team_tools.select_seat import validate, run

argument = {"seat": "1A"}
valid, reason = validate(argument)
if valid:
    result = run(page, argument, {})
    print(result)
else:
    print(reason)
```

`context` is unused but retained for the common interface. `run` also validates
defensively before reading the browser. Its only top-level result keys are
`ok` (Boolean), `message` (text), and `data` (dictionary).

Successful live result:

```json
{
  "ok": true,
  "message": "The browser confirms seat 1A is selected and Continue is enabled.",
  "data": {
    "seat": "1A",
    "selected_seat": "1A",
    "seat_message": "Selected seat 1A.",
    "continue_enabled": true
  }
}
```

The tool refuses other websites, an unready screen, missing or ambiguous visible
targets, and disabled/unavailable seats. Missing verification controls are also
rejected before clicking. Playwright errors return `ok: false`; no forced click
or retry is used.

## Reproduce the tests

Run from the repository root with Python 3.10 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python tests.py
python -m team_tests.test_select_seat --evidence evidence/team11_select_seat.json
```

On Windows, use `.venv\Scripts\activate` instead of the `source` command.
For a visible browser, add `--headed`. Direct execution also works:
`python team_tests/test_select_seat.py`.

The browser test visits only the practice website. Direct Playwright setup
selects DCA to BOS using the site's default departure date, searches, and chooses
AA101. These setup actions are not additional team tool implementations.

Each test prints its proposal, return value, independent browser evidence, and
PASS. Assertions produce a nonzero exit on failure. The optional JSON file is
also saved on an assertion failure, with the incomplete record marked failed.

## Observed results

The checked-in [JSON trace](../evidence/team11_select_seat.json) records Python,
Playwright and Chromium versions, timestamps, every call, and independent DOM
snapshots. All 12 browser cases and all 9 existing offline checks passed. The
validator also rejected all 8 malformed-input examples in the browser test.

| Browser case | Observed result |
| --- | --- |
| Before reaching the seat stage | Rejected; selection unchanged |
| Select available 1A | Exactly 1A selected; correct message; Continue enabled |
| Request unavailable 1B | Rejected; 1A and its message preserved |
| Request missing 99Z | Rejected; 1A preserved |
| Change to available 2A | Exactly 2A selected; message and Continue verified |
| Select 2A again | Same verified selection, without advancing |
| Non-dictionary argument | Rejected; browser unchanged |
| Unexpected argument key | Rejected; browser unchanged |
| Duplicate visible seat buttons | Rejected; browser unchanged |
| Hidden seat button | Rejected; browser unchanged |
| Disabled seat button | Rejected; browser unchanged |
| Missing Continue control | Rejected before selection; browser unchanged |

The last four cases deliberately modify this test browser's DOM to reproduce
problems the normal site does not present. They are not claimed as native site
behavior. The required 1A and 1B demonstrations use the unmodified live page.

The independent checker separately reads selected buttons, the message,
Continue's enabled state and stage visibility. It compares those facts against
the requested seat and the tool's output. For rejected calls it compares the
before/after snapshots, rather than accepting `ok: false` as proof of no change.

## Limitations and team participation

This tool targets the current practice site's IDs, selected CSS class, and
English confirmation message. It selects one seat, even when the search has
multiple passengers. It neither prepares the seat stage nor clicks Continue.
An error after a click can leave the browser changed; `ok: false` means the
requested result was not verified, not that a rollback occurred.

Proposed division of responsibilities, to be confirmed by both members before
submission:

- Mingyu Gao (`coldhac`): tool implementation, input validation, browser read-back
  logic, and review of the failure-handling behavior.
- Mengyu Wu: test execution, independent verification of success and failure
  evidence, reproducibility checks, and submission documentation review.

These are proposed responsibilities, not a claim that both members have already
completed their reviews. The repository's PR template requests GitHub usernames;
Mengyu Wu's username can be supplied when the team finalizes the submission.
