# Team 11: `select_seat` Tool

## Team Members
- Mengyu Wu
- Mingyu Gao

## Overview
The `select_seat` tool implements robust browser interaction for choosing an airplane seat on the Agent Airways platform using Playwright. It ensures input validity, locates and verifies the seat on the interactive seat map, executes the selection, and independently verifies the updated DOM state.

## Core Capabilities & Implementation Details
- **Input Validation**: Strips whitespace, standardizes seat identifiers to uppercase, and rejects empty or invalid non-string values before taking browser actions.
- **Dynamic Element Detection**: Locates seats using visible text and dataset attributes (`data-seat`), ensuring the seat map has loaded.
- **State & Availability Checks**: Verifies that the seat is not disabled or occupied (`disabled` attribute and `aria-disabled="true"`).
- **Independent DOM Verification**: Inspects the post-click DOM properties (`aria-checked="true"` and CSS class containing `selected`) to ensure the seat was successfully toggled in the live browser rather than assuming success after the click action.

## Testing Strategy
The automated test suite in `team_tests/test_select_seat.py` covers both success and failure paths:
1. **Normal Case (`test_select_seat_normal`)**:
   - Navigates through the wizard form (search -> select flight -> seat selection).
   - Dynamically discovers an available seat from the rendered seat map.
   - Executes `select_seat` and asserts successful execution and DOM state confirmation.
2. **Failure Case (`test_select_seat_failure`)**:
   - Attempts to select a non-existent seat identifier (`NON_EXISTENT_999`).
   - Asserts that a `RuntimeError` is raised indicating the target does not exist or the map is unavailable.

## Test Results
Executing pytest across the test suite confirms both test cases pass:

team_tests/test_select_seat.py::test_select_seat_normal PASSED
team_tests/test_select_seat.py::test_select_seat_failure PASSED
2 passed in 4.57s

## Known Limitations
- The tool requires the booking interface to have advanced past the initial flight search and flight selection stages so that the seat selection map is present in the DOM.
- If identical seat identifiers appear in multiple cabin sections without unique locator scoping, the tool targets the first matching available element.