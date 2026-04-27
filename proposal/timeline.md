# Timeline

**Proposed engagement duration:** 5 weeks
**Estimated start:** May 19, 2026 (two weeks post-award)
**Estimated completion:** June 20, 2026

---

## Phased Delivery Plan

### Week 1 — Onboarding & R4 Architecture Docs
- Engagement kickoff with R. Tanaka and IT
- Confirm defect list for R1, agree scope for R3 critical flows
- Full codebase review
- Deliver architecture documentation (R4) — early delivery gives Meridian IT visibility before changes begin

**Milestone:** Architecture doc delivered; defect list confirmed

---

### Week 2 — R1 Reports Remediation
- Fix all confirmed Reports module defects
- Wire filters end-to-end; resolve i18n gaps
- Weekly check-in with operations team to validate

**Milestone:** Reports module passes acceptance criteria; check-in sign-off from Tanaka's team

---

### Week 3 — R2 Restocking (Backend + API)
- Implement `/api/restock/recommendations` endpoint
- Restock logic: inventory vs. demand forecast, budget ceiling, ranked output
- Unit-level API verification

**Milestone:** Restocking API returns correct recommendations for test cases

---

### Week 4 — R2 Restocking (Frontend) + R3 Testing
- Build Restocking view in Vue
- Wire to API; validate budget input and recommendation display
- Begin Playwright test suite; cover inventory, orders, Reports flows

**Milestone:** Restocking view functional end-to-end; core test suite passing

---

### Week 5 — R3 Testing (Restocking) + Buffer + D-items
- Add Restocking view tests
- Documentation review; final QA pass
- D2 (i18n extension) delivered if R1–R4 on track
- D3 (dark mode) if schedule permits
- Final delivery and handoff call

**Milestone:** Full test suite passing; all R-items delivered; handoff documentation complete

---

## Weekly Cadence

- **Monday:** Async status update to J. Okafor and R. Tanaka
- **Wednesday:** Working session with operations team (as needed for R2 validation)
- **Friday:** Weekly written check-in; flag any scope questions

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| R1 defect count higher than expected | Medium | Audit in Week 1 before committing to fixed scope; escalate if materially beyond eight issues |
| R2 restock logic requires business rule clarification | Low–Medium | Confirm assumptions at kickoff; operations team available for questions |
| IT environment constraints for R3 test run | Low | Document run command in Week 4; IT review before final delivery |
| D1 direction unavailable by Week 2 | Medium | Proceed without D1 rather than delay R-items |
