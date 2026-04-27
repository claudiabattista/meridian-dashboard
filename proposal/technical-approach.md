# Technical Approach

---

## Assumptions

The RFP package includes the previous vendor's handoff notes and source code. Our technical approach is based on a review of both. Where the RFP leaves scope open, we have made the following assumptions — we will confirm these at engagement kickoff:

- **R1 (Reports):** We will treat the codebase as the source of truth for defects. "At least eight issues" means we will audit and fix everything we find, not work from a fixed list.
- **R2 (Restocking):** Budget ceiling is an operator-supplied input per session (not a persisted setting). Reorder logic: flag any SKU where current stock falls below 30 days of forecasted demand; rank by urgency; cap total recommended spend at the supplied ceiling.
- **R3 (Testing):** "Critical user flows" means: inventory browse and filter, order status view, Reports module, and the new Restocking view. We will confirm scope with IT at kickoff.
- **R4 (Architecture docs):** Delivered as an HTML document with a visual diagram, suitable for browser viewing without tooling.

---

## R1 — Reports Module Remediation

The previous vendor acknowledged the Reports module was incomplete at contract end. Our approach:

1. **Audit first.** Before touching code, we will enumerate every defect — filter wiring, i18n gaps, data pattern inconsistencies, console noise. We will produce a short defect list and share it with Meridian before beginning fixes, so there are no surprises about scope.
2. **Fix systematically.** Filters will be wired end-to-end (Vue → API client → FastAPI query params → filtered response). Each fix will be verified against the running application, not just in isolation.
3. **Verify i18n parity.** Any strings exposed in the Reports view will be confirmed in the translation files. Gaps will be filled; we will not ship views with untranslated strings.

Acceptance criterion: every filter on the Reports page produces correct results; no console errors; all visible strings are translation-ready.

---

## R2 — Restocking Recommendations

This is new functionality, built alongside the existing system without disrupting it.

**Backend.** A new `/api/restock/recommendations` endpoint will accept a `budget` parameter and return a ranked list of recommended purchase orders. Logic: cross-reference current inventory levels against the demand forecast; surface SKUs below the 30-day threshold; rank by days-of-stock remaining; cap total recommended spend at the supplied budget.

**Frontend.** A new Restocking view in the existing Vue app, consistent with the current design system (slate/gray palette, CSS Grid layout). The operator inputs a budget ceiling; the view displays recommended orders with SKU, warehouse, current stock, recommended quantity, and estimated cost. Totals update as the operator adjusts the budget.

**No database required.** The existing JSON-backed data model is sufficient for this feature. We will not introduce a database dependency in this engagement.

---

## R3 — Automated Browser Testing

Meridian's IT team has blocked changes to the system due to the absence of test coverage. We will establish a Playwright end-to-end test suite covering:

- Inventory view: load, warehouse filter, category filter
- Orders view: status filter, month filter
- Reports module: all repaired filters
- Restocking view: budget input, recommendation display

Tests will run against the local development server. We will document the run command so IT can execute them as part of any future change review.

---

## R4 — Architecture Documentation

We will deliver a current-state architecture overview as a self-contained HTML file. It will cover:

- System components (Vue frontend, FastAPI backend, JSON data layer)
- Data flow from user interaction to API response
- Filter system mechanics
- File map for key source files
- Known constraints and recommended next steps (e.g., database migration path if Meridian outgrows the JSON layer)

Intended audience: Meridian IT staff who did not build the system. Written for orientation, not deep technical reference.

---

## Desired Items (D1–D3)

We include the following assessment of the desired items for Meridian's evaluation:

- **D1 (UI modernization):** The current design system is functional and coherent. A visual refresh is achievable within the engagement timeline if Meridian can provide direction on target standards (a reference design or brand guide) by end of Week 2.
- **D2 (i18n extension):** The codebase already uses Vue i18n. Extending coverage to remaining modules — particularly for the Tokyo team — is straightforward once R1 is complete and establishes the pattern. We include this in scope at no additional cost if R1–R4 are completed on schedule.
- **D3 (Dark mode):** Operator-selectable theme via CSS custom properties. Achievable as a stretch item in Week 5 if the core deliverables are on track.

D1–D3 are not guaranteed deliverables. We will communicate status at the Week 3 check-in.
