---
name: "production-readiness"
description: "Pre-launch production readiness review (PRR) for Luke's apps. The aggregated go-live checklist: legal traps, billing, reliability, and UX, distilled from viral builder checklists plus Luke's own standing rules. Run before any app takes money or is declared production-ready. Trigger on: 'production readiness', 'PRR', 'pre-launch check', 'go-live checklist', 'ready for production'."
---

# Production Readiness Review (PRR)

## Purpose
The last gate before an app goes live or takes money. One checklist, every dimension that kills launches: legal, billing, reliability, UX. Distilled from builder checklists Luke saves (each new one gets appended below with source + date — never replace, only add). This is risk-spotting, not legal advice.

## How to run it
1. Read the app source (not the marketing copy).
2. Go through every section. Each item gets PASS / FAIL / N-A with file:line evidence. No vibes.
3. Every FAIL becomes a work item with severity: **P0** (fix before any launch), **P1** (fix before taking money), **P2** (fix within 2 weeks post-launch).
4. End with a ship / no-ship verdict.

## Section 1 — Legal traps (distilled 2026-10-08 from @LimestoneHQ "10 legal traps hiding in vibe-coded apps")
Not legal advice. Route P0s to a lawyer.
- **Public database / keys in frontend:** no API keys, secrets, or tokens in client code; no public-read database without row-level security. (Researchers found 170 vibe-built apps leaking user data — triggers state breach-notice laws.)
- **Privacy policy:** exists, linked in-app, and matches what the code actually collects/transmits. (CA: $2,500/violation; Apple/Google Play reject without one.)
- **Kids:** any under-13 users or kid-appealing content needs COPPA parental consent + age gate. ($53,088/violation.)
- **Session replay:** no FullStory/Hotjar/LogRocket-style keystroke recording without explicit consent. (CA wiretap claims: $5,000/violation.)
- **Health data:** no tracking pixels (Meta, Google) on pages/flows touching health data. (GoodRx $1.5M, BetterHelp $7.8M.)
- **Marketing email:** every marketing email has one-click unsubscribe + postal address. (CAN-SPAM: up to $53,088/email.)
- **Auto-renewal:** renewal terms clear and conspicuous AT checkout, next to the button — not buried. (CA treats bad renewals as gifts = refunds; ROSCA.)
- **AI disclosure:** if any chatbot or feature could be mistaken for a human, disclose it's AI. (EU AI Act: up to €15M or 3% turnover; California companion-chatbot law.)
- **Accessibility basics:** alt text on meaningful images, labels on all inputs, keyboard navigation works. (3,117 federal suits in 2025, up 27%.)
- **DMCA:** user uploads (photos, avatars, content) need a registered DMCA agent ($6) + takedown process, or no safe harbor. (Up to $150K/work if willful.)
- *Deeper version of most of these lives in the `security-review` skill — run that too before store submission.*

## Section 2 — Billing and money (Luke's Stripe setup)
- Trial config matches the trial strategy: 14 days, full-featured, no card at signup (test mode first, live only when Luke says).
- Prices in Stripe match prices shown in-app. Lookup keys correct.
- Webhook endpoint registered, signatures verify, failure states tested (card declined, trial expired, canceled).
- Billing failures fail OPEN for the app (friendly copy, user data untouched). No raw error codes to users.
- Refund path exists and is documented (30-day money-back guarantee).

## Section 3 — Reliability
- Works offline where the PRD says it must; honest offline banner where it can't.
- Every network call has loading, error, and retry states. No silent spinners, no dead ends.
- No console errors, no unhandled promise rejections (Playwright `pageerror` listener, zero tolerance).
- Rate limits on abuse paths (device registration, trial start, uploads). Upload quotas set.
- Secrets only as server-side env vars; client bundle grepped clean.

## Section 4 — UX before launch (from the sweep's UI quality bar)
- Bottom-tab nav (3–5 labeled items); next-job-first home; core money task in ≤3 taps.
- 16px+ inputs, 44×44pt tap targets minimum (56pt+ for glove-primary actions), 4.5:1 text contrast.
- Empty/loading/error/offline states all designed. Forms autosave drafts.
- No em dashes in copy. Bespoke SVG icons, no emoji in chrome. Copy matches behavior (honesty axis).

## Section 5 — Pre-launch prompt checklist (distilled 2026-10-08 from @suraj_sharma14 "Every vibe coder's pre-launch prompt: 20 things")
Paraphrased, not verbatim. Items already covered elsewhere in this skill are marked.
- [ ] API keys out of frontend code and git; rotate any key ever committed. (New: the rotation rule.)
- [ ] Rate limiting enabled on auth and abuse paths. (Covered: Section 3.)
- [ ] Auth enforced on every route server-side, not just hidden in UI.
- [ ] Database rules: users see only their own data. (Covered: Section 1 RLS item.)
- [ ] All input validated server-side.
- [ ] AI-provider spending capped with alerts. (New: billing guardrail — set caps, not just hope.)
- [ ] Stack traces stripped from client-facing errors; generic messages + correlation IDs. (New as a checklist item.)
- [ ] Error tracking wired. (Covered: Section 3.)
- [ ] Database backed up AND a restore tested. (New: untested backups don't count.)
- [ ] Styled 404/500 pages. (New.)
- [ ] Works on cheap Android phones, not just a new iPhone. (New: low-end device pass.)
- [ ] Nothing on the critical path loads slower than 3 seconds. (New: performance budget.)
- [ ] Meta tags + OG image so shared links look right. (New.)
- [ ] Privacy policy + terms. (Covered: Section 1.)
- [ ] Analytics for drop-off tracking. (New: PRD decides events; PRR verifies they're live.)
- [ ] End-to-end test: signup, payment, password reset. (New: the auth trilogy.)
- [ ] Transactional emails avoid spam (SPF/DKIM/DMARC set). (New.)
- [ ] A visible way for users to contact the human behind the app. (New.)
- [ ] Written rollback plan for launch day. (New: what we do if the deploy breaks at 9pm.)

## Operating rules
1. Append, don't rewrite. New checklists get a new dated section with source.
2. Every item needs evidence: file:line or "verified live at URL".
3. Never invent a penalty number; use the ones recorded here or say "varies".
4. A clean PRR is a result. Say so plainly and ship.
