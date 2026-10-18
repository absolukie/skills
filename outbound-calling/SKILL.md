---
name: "outbound-calling"
description: "Place outbound AI phone calls through either of Luke's two proven calling paths: ElevenLabs + Twilio, or ElevenLabs + Telnyx SIP trunk. Trigger on: 'call them', 'have the agent call', 'place a call', outbound calling setup, or checking call usage."
---

# Outbound Calling

Luke has two working outbound-call paths. Both use ElevenLabs Conversational AI
as the voice agent; they differ in the PSTN carrier.

## The two paths

### Path A: ElevenLabs + Twilio

- Twilio account: sid/token stored as `TWILIO_SID` / `TWILIO_TOKEN` on the
  `sprint-backend-proto` worker. Default caller id: `TWILIO_FROM=+19255550100`.
- Setup (verified 2026-10-08): create the ElevenLabs agent, provision a Twilio
  US number, verify the destination number on Twilio, import the Twilio number
  into ElevenLabs, then trigger the call.
- Trigger: ElevenLabs dashboard, or `POST /v1/convai/twilio/outbound-call`
  (agent_id, agent_phone_number_id, to_number).
- Dynamic variables go through the API only (verified 2026-10-13): the
  dashboard "Send Test Call" dialog has NO variable fields at all, even with
  the right agent selected. In the dashboard the only variable-capable route
  is a batch-call campaign. For a single call, POST with
  `conversation_initiation_client_data.dynamic_variables` carrying the values.
- IVR navigation (learned the hard way 2026-10-13, IRS callback line): when
  the callee is a speech-recognition IVR, the agent must answer menu prompts
  with ONLY the bare digits or word requested, no sentences, no name, and no
  bracketed emotion tags. Sentence-style answers ("I was given extension six
  three three, I will enter that now") failed the IRS IVR's parser three
  times and got the call hung up on. Put the bare-answer rule in the agent
  prompt before any IVR call.
- IVR timing (verified 2026-10-13, second IRS attempt): one keypad entry
  per system prompt, then silence until the system speaks again. The agent
  sent the extension tones and immediately stacked the SSN tones on top
  before the IVR responded; the IVR glued the streams together, read the
  first SSN digits as an invalid extension, and killed the call in 31
  seconds. Also: stay silent through greetings, and enter each value only
  when the system explicitly asks for that specific value, never early.
- Some IVRs do not register the agent's tones at all (verified 2026-10-13,
  IRS): across three calls the IRS speech IVR never accepted a tone entry
  (extension or SSN), while spoken answers worked every time. On the fourth
  IRS call, spoken digits carried the whole verification: the extension,
  SSN, ZIP, and date of birth were each accepted and read back for
  confirmation. When an IVR says "say or enter", go spoken-first: bare
  digits, one at a time, short pauses, nothing else in the turn. Keep tones
  as the fallback, not the default, for speech-first government IVRs.
- DTMF needs the tool, not just prompt text (verified 2026-10-13): an agent
  whose prompt says "enter via DTMF" still cannot send tones unless the
  `play_keypad_touch_tone` system tool is in the agent prompt's `tools` list
  ({type: "system", name: "play_keypad_touch_tone", params:
  {system_tool_type: "play_keypad_touch_tone"}}). The IRS Refund Caller
  shipped with tools=[] and only spoke about entering digits; enabling the
  tool via PATCH fixed it. Check the tools list, not the prompt prose,
  before any call that needs keypad entry.
- Watch for trial limits: on a Twilio trial, calls only reach verified
  destination numbers and the called party hears a trial announcement that
  requires a keypress. Check the account tier before any real call.

### Path B: ElevenLabs + Telnyx SIP trunk (China)

- Telnyx account: absolukie@gmail.com, paid tier. Number +1 213 727 0940
  (purchased Oct 8, 2026; corrected Oct 15, 2026 against the live Telnyx portal: +1 213 555 0100 was never on the account). SIP trunk "ElevenLabs AI Voice" points at
  `sip.rtc.elevenlabs.io:5060` (TCP, E.164), on the Default outbound voice
  profile, imported into ElevenLabs as a Telnyx SIP trunk
  (`phnum_7501m4fge9bgfz1s4ccr8dtmzq5v`).
- Proven 2026-10-09: the Fu 1088 booking call (109s, Mandarin) went through
  this path end to end, including mainland-China (+86) dialing. The Xinrongji
  booking call connected on the first attempt the same day.
- Trigger: ElevenLabs SIP outbound-call API using a restricted key with
  ConvAI / ElevenAgents write scope (the existing one is named
  "ConvAI SIP Call"), or the ElevenLabs dashboard with the Telnyx number
  selected as the caller id.

## Which path when

- US calls where SMS may follow, or anything tied to Curbside: Twilio.
- **Telnyx is China-only.** Standing rule from Luke (2026-10-09): only use the
  Telnyx SIP path for mainland-China calls. Everything else goes through Twilio.
- **Twilio cannot call China at all.** +86 is absent from Twilio Voice Geo
  Permissions (both risk tabs) and from the console country list. Never route
  a China call through Twilio.
- When in doubt, ask Luke which number should show as caller id.

## ElevenLabs account notes

- Sign-in is Google SSO for absolukie@gmail.com; the workspace is
  "Luke's Workspace". The managed browser session may already be signed in
  (it persisted across the Oct 9 Xinrongji runs). Check the dashboard state
  before assuming a sign-in blocker; earlier "blocked" reports were stale
  sessions, and one retry run placed zero calls over a sign-in that turned
  out to already be active.
- If logged out (Luke, 2026-10-13): just log back in with Google SSO as
  absolukie@gmail.com. It usually goes straight through and will not ask
  for a confirmation; do not stop to ask Luke first.
- API keys: create a restricted key scoped to ElevenAgents / ConvAI write
  only, one per purpose. Raw key values are never stored in chat, files, or
  this skill; use them transiently.
- Getting a key mid-task (proven 2026-10-13): the sandbox cannot use the
  stored `custom.elevenlabs` connector credential (surrogate returns 403,
  policy points at a privsep tool that does not exist for ElevenLabs). The
  working route: in the signed-in dashboard go to Settings > API Keys,
  create a restricted key (ElevenAgents Write, everything else No Access),
  and pass the value to scripts through an environment variable only. Luke
  authorized creating the key directly ("you can get the API yourself",
  2026-10-13) on top of his standing sign-in permission.
- Call monitoring (proven 2026-10-13): after triggering, poll
  `GET /v1/convai/conversations/<conversation_id>` every ~45s until status
  is done or failed. Tolerate transient network drops and keep polling; a
  crashed poller does not affect the call. The finished object carries
  metadata.call_duration_secs, analysis.call_successful, and
  analysis.transcript_summary; the full transcript is in the same object.
  Working scripts: `~/workspace/calling/el_call_now.py` (verify agent and
  phone, parse values from the private prompt file, place the call, save
  the conversation_id) and `~/workspace/calling/el_poll.py` (poll to
  completion and write the result JSON).

## Agent prompt rules (Luke's standing rules, all calls)

1. **Neutral caller.** The agent opens as a neutral caller asking to book.
   No self-introduction, no announcing who sent it.
2. **Never mention AI, an assistant, or automation.** Not in the opening, not
   mid-call. The only exception: if the other side directly asks who is
   calling, the agent may say it is Zhang Lukun's assistant (the approved
   assistant line). It never claims to be Luke himself.
3. **Book under Zhang Lukun** (张路坤). Restaurant bookings use his Chinese
   name and his restaurant contact number.
4. **Conciseness rule, verbatim on every agent:** "Say only what is
   necessary. Keep every reply short. Avoid repetition and extra
   pleasantries." (Published and read-back verified on the Fu 1088 Booker
   and Xinrongji Booker, 2026-10-09.)
5. **Draft the prompt first, Luke reviews it.** Never place a call without
   Luke's explicit go-ahead naming the destination and the purpose.
   "Draft the prompt" is not "make the call." Save prompt drafts under
   `~/workspace/calling/`.
6. **Sensitive values** (SSN, DOB, account numbers, WeChat ID) go in
   `{{variables}}` injected at call time, or in the live agent prompt when
   the call requires speaking them; never hardcode them into a saved draft
   file or this skill.
7. The agent never invents facts it was not given: no made-up times,
   party sizes, or fallback offers beyond what the prompt authorizes.

## China calling specifics

- **Timing is the number-one failure mode.** Beijing restaurants typically
  answer 11:30 AM to 2:00 PM and 5:30 PM to 9:00 PM Beijing time. Attempts
  landing around midnight Beijing time time out with no answer because the
  restaurant is closed; that is a scheduling error, not a wrong number.
  Schedule the run for just after a service opening.
- **Busy lines are normal.** SIP 486 User Busy on a popular restaurant is
  expected. Retry pattern: up to 3 attempts spaced about 20 minutes apart,
  staying inside service hours.
- **Language:** agents for China restaurants speak Mandarin, first person,
  short replies.
- **Deposits: never authorize or pay.** If the restaurant requires a deposit
  (for a reservation or a pre-order dish), the agent collects the exact
  terms: amount, payment method (WeChat transfer, payment link, bank
  transfer), and deadline, then ends politely and reports to Luke. Payment
  is always Luke's separate decision.
- **WeChat coordination:** Luke has an official WeChat he is comfortable
  sharing with restaurants for deposit and menu coordination (confirmed
  2026-10-09). Check first, spell only if needed (Luke's correction,
  2026-10-11): the agent first asks what WeChat ID the restaurant already
  has on record and has them read it back; if it matches, there is no need
  to give it again. Only if they have no record or read it wrong does the
  agent spell it out character by character and repeat it. The agent may
  reference any WeChat message Luke already sent so the restaurant can
  connect the two.
- **Branch discipline:** chain restaurants can have several Beijing or
  Shanghai locations with different ratings. Verify the exact branch and
  its own phone number from an independent listing before calling; never
  substitute another branch's number.

## Proven calls (reference)

- Test call, 2026-10-08: "Test Caller" agent, ElevenLabs + Twilio,
  105 seconds, 21 turns, transcript confirmed.
- Fu 1088 (Shanghai), 2026-10-09: ElevenLabs + Telnyx, 109 seconds,
  Mandarin. Booked table for 4, Dec 6, 2026, 9:30 PM under 张路坤
  (7:30 and 8:00 PM were full). Min spend ¥500 per person, no deposit.
- Xinrongji Xinyuan South Road (Beijing, Michelin 3-star), 2026-10-09:
  ElevenLabs + Telnyx, connected first attempt. Confirmed Sunday
  Dec 13, 2026, 6:30 PM, 4 adults, main hall, under 张路坤; restaurant
  read the details back. No deposit paid or stated.

## After a call

1. Report to Luke: who was reached, the outcome, duration, cost, and
   anything needing his direct follow-up.
2. **PII hygiene:** call transcripts and recordings get the `audio-redact`
   treatment before anything is published or stored long-term. Raw
   recordings stay out of the repo.
3. Update the relevant tracked item and MEMORY.md with the confirmed
   outcome the same day, and correct any earlier pending state so a stale
   "not booked" note never survives a successful call.

## Cost awareness

- Telnyx draws from a small prepaid credit ($5 added 2026-10-08); Twilio
  draws from its account balance; ElevenLabs from its credit pool.
- Check balances before a batch of calls. Report per-call cost after
  test calls.

## Usage checks

- ElevenLabs: dashboard billing/usage (signed in as Luke Zhang).
- Twilio: console billing overview.
- Telnyx: portal balance and call history.
