# D&D (Debug Dialogue)

A collaborative debugging pattern for when something looks wrong and the user wants to work through it together, not just get a fix. Like a D&D session: you investigate together, roll for insight, and decide the next move as a party.

## When to use

User shows you a bug (often with a screenshot) and wants to understand what's happening, not just have you patch it silently. They'll ask questions like "what do you think I want", "what's in the code right now", or "does X look like Y". They want to see your reasoning.

## The pattern

1. **Investigate the actual assets, don't guess.** If the user says the visual is wrong, extract the real files and look at them. Render the SVG paths. Pull frames from the video. Read the actual code. Never speculate about what "might" be wrong.

2. **Report honestly, including bad news.** If the video is corrupted, say so. If the data is wrong, say so. Show the evidence (rendered images, frame extracts, code snippets). Don't soft-pedal.

3. **Let the user drive the questions.** They'll ask:
   - "Put what you think I want in your own words" → Articulate their goal back, plainly. Check your understanding before building.
   - "What is currently in the code for X" → Show the actual code state. What the paths are, how they're ordered, how they got there.
   - "Does X look like Y" → Test it. Render it. Give a yes/no with evidence.

4. **Discuss options before building.** When you hit a fundamental problem (wrong data, corrupted file), lay out the real options with tradeoffs. Let them pick the direction. Don't unilaterally swap implementations.

5. **Name the uncertainty.** If the stroke order is your best guess, say so. If you can't verify something, say what you verified and what's still unknown.

## What not to do

- Don't replace the user's chosen approach (video → SVG) without asking, even if you think the replacement is better.
- Don't claim something works because the code looks right. Verify with real rendering.
- Don't bury the key finding in technical detail. Lead with the plain-language answer.

## Example flow

User: "You are joking look at this" + screenshot
You: Investigate the actual rendered output, compare against expected
User: "Put what you think I want in your own words"
You: Articulate their goal plainly, confirm before acting
User: "What is currently in the code for the SVGs"
You: Show the actual paths, order, and how the order was determined
User: "Do the SVGs look like the ghost outline"
You: Render all paths together, compare, give honest yes/no with the image
User: Picks a direction from options you laid out
