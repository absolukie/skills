---
name: "security-review"
description: "Pre-publish legal and security risk audit for Luke's apps. Run before any App Store / Google Play submission, and before marking a projects-hub project 'verified'. Trigger on: 'security review', 'legal audit', 'pre-publish check', 'audit this app', 'ready to verify'."
---

# Security Review

## Purpose
Catch the legal, privacy, and store-policy risks that turn a shipped app into a liability. This is risk-spotting, not legal advice: every HIGH finding should go to a real lawyer before launch.

## Workflow
1. **Identify the app surface.** Read the source (not the listing): what it does, what data it touches, what it sends over the network, what it charges for.
2. **Run the six-traps checklist** (from the Oct 2026 viral post that created this skill). Each gets PASS/FAIL with file+line evidence:
   - **Age gate / COPPA:** any signup or account flow? Any personal info from under-13s? No gate + kid-appealing app = up to $53K per child.
   - **Third-party leaks:** Google Fonts or any CDN assets leaking visitor IPs (GDPR)? Grep HTML/CSS/JS for external URLs. House rule: vendor everything.
   - **Session replay:** FullStory / Hotjar / LogRocket / any keystroke recording? (CA CIPA wiretapping risk, $5K per session.)
   - **Email:** any marketing or transactional email? Needs unsubscribe link + postal address (CAN-SPAM, up to $53K per email).
   - **Subscriptions:** any auto-renewal without renewal terms next to the button? (CA treats bad renewals as gifts = refunds.)
   - **DMCA:** any user uploads (avatars, images, content)? Needs a registered DMCA agent ($6) + takedown process, or no safe harbor ($150K per work).
3. **Run the app-risk checklist:**
   - **Gambling:** real-money wagering, prizes, entry fees, or purchasable virtual currency in a chance game? (Rummy, poker, slots are store-sensitive categories.)
   - **Privacy vs reality:** does `privacy.html` match what the code actually collects and transmits? Check analytics, ads SDKs, crash reporters, and what the server sees (IP/UA count as personal data under GDPR/CCPA).
   - **Secrets:** hardcoded API keys, tokens, or credentials in client code? (`grep -riE 'api[_-]?key|secret|token|password'` — exclude comments.)
   - **Terms of Service:** does a ToS/EULA exist and is it linked in-app? Apple has a default EULA; Google Play does not.
   - **IAP honesty:** does the listing match reality ("No ads" + remove_ads IAP = deceptive)? One-time vs subscription labeled correctly? Price shown pre-purchase? Restore Purchases present?
   - **IP:** app name trademark-cleared (USPTO TESS + store search)? Third-party art/sounds/fonts licensed? Real brand names in content (nominative use is usually fine, no logos/endorsement claims)?
   - **Store policy:** Apple 4.2 minimum functionality (no plain webview wrappers), gambling policy, privacy nutrition labels / Data Safety declarations match code.
   - **Listing honesty:** do all listing drafts agree with each other and with the app? Retire stale drafts.
4. **Verify, don't assume.** Every FAIL needs file path + line number. If the code can't confirm it, mark it UNVERIFIED, not PASS.

## Output Contract
A findings list, each with: **severity** (HIGH = fix before ship, MEDIUM = fix before submission, LOW = fix when convenient), **category**, **evidence** (file:line), **why it matters** (the penalty or rejection in plain words), **fix** (concrete next step). End with a ship/no-ship verdict and the priority fix list. Save the full report to `~/workspace/release/legal-audit-<app>.md`.

## Operating Rules
1. Read code, not marketing copy. The listing is a claim; the source is the truth.
2. No finding without evidence. Grep hits beat vibes.
3. Never invent a penalty number; use the ones in this skill or say "varies".
4. This is not legal advice: say so in the report, and route HIGHs to a lawyer.
5. When the app passes clean, say so plainly. A clean audit is a result, not a failure to find things.
