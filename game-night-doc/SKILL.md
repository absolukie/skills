---
name: "game-night-doc"
description: "Build a self-contained game night (or event night) Google Doc: timed schedule at the very top, transit both ways, food options with photos of the food only (unique items, no people), and venue maps annotated with a red circle around the seats. Trigger on: 'game night doc', 'event doc', 'put together a doc for the game', or any request for a single doc that holds a whole arena or event night plan."
---

# Game Night Doc

## Purpose
One Google Doc that holds an entire event night, so the reader never has to leave it: the timed schedule, how to get there and back, what to eat (with photos), and where the seats are (maps, circled).

## Structure, in this order
1. Title and date.
2. **The full timed schedule at the very top**: every step from leaving home to the last ride home, bold time plus bold step lead.
3. Basics: event time, doors, section/row/seats, mobile ticket and wallet note, ticket perks, bag policy.
4. Getting There: the full transit chain with a recommended option, a relaxed option, and the latest workable option, each with exact times.
5. Food Plan: Best Food Options first (numbered, dishes as bullets, photos under each), then Other Options (bold-lead bullets, one photo each).
6. Maps: official venue portal/concourse map first, then seating charts, each with a caption that says what is circled.
7. Getting Home: postgame items first, then the main return option, backups, and the last departure of the night.
8. Reminders: tickets ready, arrive early, availability may change, budget per person, enjoy it.

## Research rules
- Event basics (doors, bag policy, ticket perks) come from the venue's official pages, not roundup articles.
- Transit times come from the transit agency's official timetable for the correct service day. Give the main pick, backups, and the last departure of the night for the return leg. State fares as approximate unless the fare table settles them.
- The food list comes from the venue's official food and beverage page (stand names, portal or gate numbers, dishes).

## Photo rules (the hard-won part)
- **Food photos only: the dish itself. Never people, never decor, never stand exteriors or interiors.**
- **Every photo is a unique item.** Never two photos of the same item, and never the same photo twice in one doc. A stand famous for a single item gets ONE photo.
- Watch for near-duplicates across stands: venue food programs reuse hero shots (the same hot dog tray photo served two different stands at two resolutions in the first build of the doc this skill came from). Compare candidates by eye before filing.
- Prefer official venue and vendor photos. When no real photo of a stand's dish exists, a clearly-flagged approximate is allowed; flag approximates honestly in the delivery message, never in a caption that implies it is the dish.
- Keep a manifest next to the images: file, stand, subject, source URL, exact or approximate.
- Verify every download is a real image (magic bytes, not an HTML error page). Word documents take JPEG or PNG, not WEBP. Re-encode progressive JPEGs to baseline: python-docx rejects progressive files with UnrecognizedImageError.
- Download at the highest resolution offered; downscale anything huge (over about 1600 px wide) before embedding.

## Map annotation
- Use the venue's official portal map if one exists. Search first suggests only seating charts and photos; the real portal map usually exists (venue and map-reseller sources carry it). Keep looking before settling for a photo of a concourse.
- Annotate COPIES, never the originals: locate the section with visual grounding, draw a red ellipse around it plus a bold red section number beside it (PIL, white halo behind the number for legibility), and read the result back to confirm the circle sits on the right section.
- Captions say what the circle is: "Section NNN is circled in red", with the row and seats named.

## Build and QA
- Generate the .docx with a python-docx script, never by editing the binary. Real heading styles, real list styles, and set the document core title property.
- Match photos to stands by FILENAME PREFIX, never by stand-name substring: substring matching double-booked photos when one stand's name contained another's (a plain "City Bistro" key also matched "Lagunitas City Bistro").
- Validate before uploading: convert the .docx to PDF with headless LibreOffice, rasterize every page, and read every page image. The rendered pages are the only check that catches photo mixups.

## Publish to Google Docs
- Create the empty doc once (Google Docs API `documents.create`) and CAPTURE the documentId from that response. Re-running create to "see the id again" creates a duplicate; if that happens, list files by title, keep one, trash the rest, and confirm the owner is the account the user named.
- Fill it with a Drive `files.update` media upload of the .docx. The upload replaces the whole body and keeps the same doc link, so later revisions go to the same URL.
- Read back with `documents.get` and verify: image count matches the manifest, the schedule heading appears before the basics, and the key facts are present. Deliver the link only after the read-back passes.

## Delivery
The doc link on its own line, a short list of what is inside, and honest notes on any approximate photos.
