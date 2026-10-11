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
- Watch for trial limits: on a Twilio trial, calls only reach verified
  destination numbers and the called party hears a trial announcement that
  requires a keypress. Check the account tier before any real call.

### Path B: ElevenLabs + Telnyx SIP trunk

- Telnyx account: absolukie@gmail.com, paid tier. Number +1 213 555 0100
  ($1/mo). SIP trunk "ElevenLabs AI Voice" points at
  `sip.rtc.elevenlabs.io:5060` (TCP, E.164), imported into ElevenLabs as
  "Telnyx +1 213 555 0100" (`phnum_7501m4fge9bgfz1s4ccr8dtmzq5v`).
- Proven 2026-10-09: the Fu 1088 Beijing booking call (109s, Mandarin) went
  through this path end to end, including mainland-China (+86) dialing.
- Trigger: ElevenLabs SIP outbound-call API using the "ConvAI SIP Call" key
  (ConvAI write scope), or the ElevenLabs dashboard with the Telnyx number
  selected as the caller id.

## Which path when

- US calls where SMS may follow, or anything tied to Curbside: Twilio.
- **Telnyx is China-only.** Standing rule from Luke (2026-10-09): only use the
  Telnyx SIP path for mainland-China calls. Everything else goes through Twilio.
- When in doubt, ask Luke which number should show as caller id.

## Rules

1. **Never place a call without Luke's explicit go-ahead naming the destination
   and the purpose.** "Draft the prompt" is not "make the call."
2. **Draft the agent prompt first, he reviews it.** Save drafts under
   `~/workspace/calling/`. Sensitive values (SSN, DOB, account numbers) go in
   `{{variables}}` injected at call time, never hardcoded into a saved agent.
3. The agent identifies itself truthfully as calling on Luke's behalf. It never
   claims to be Luke, and never invents facts it was not given.
4. **PII hygiene:** call transcripts and recordings get the `audio-redact`
   treatment before anything is published or stored long-term. Raw recordings
   stay out of the repo.
5. **Cost awareness:** check balances before a batch of calls. Telnyx draws
   from a $5 prepaid credit; Twilio from its account balance; ElevenLabs from
   its credit pool. Report per-call cost after test calls.
6. After a call: report who was reached, the outcome, duration, cost, and
   anything needing Luke's direct follow-up.

## Usage checks

- ElevenLabs: dashboard billing/usage (signed in as Luke Zhang).
- Twilio: console billing overview.
- Telnyx: portal balance and call history.
