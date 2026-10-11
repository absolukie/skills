# bottom-sheet-drag-lock

Lock drag gestures inside a bottom-sheet webview so downward drags stay in the game instead of pulling the native sheet down.

## When to use

Any game or interaction that requires dragging (especially downward) inside a website bottom sheet / webview. If a downward drag on the page yanks the whole native sheet instead of moving the game, this skill is the fix. Applied 2026-10-09 to star-salvage, icon-match, and dungeon-dash after Luke reported exactly that.

## The problem

A native bottom sheet hosting a webview claims downward drags for itself (sheet drag / dismiss). If the web page can scroll, bounce, or hand the gesture to the OS, the game loses the drag and the whole sheet moves.

## The fix (4 parts, all of them)

**1. Lock the page to the viewport.** No page scroll, no overscroll, no bounce for the sheet to grab onto:

```css
html, body{
  margin:0; padding:0;
  overscroll-behavior:none;
  position:fixed; inset:0; width:100%;
  overflow:hidden;
}
```

**2. Own the drag surface.** The canvas / stage / draggable element gets:

```css
#stage{ touch-action:none; }
```

`touch-action:none` tells the browser (and the webview) that every touch on this surface belongs to your pointer handlers. Without it, the downward drag is a scroll gesture and the sheet wins.

**3. Kill the default touch behavior.** A non-passive `touchmove` listener that prevents default. For full-screen games with no scrollable content, document-level is simplest:

```js
document.addEventListener("touchmove", function(e){ e.preventDefault(); }, {passive:false});
```

**4. Block iOS gesture events.** Pinch/rotate gesture starts can also escape to the container:

```js
document.addEventListener("gesturestart", function(e){ e.preventDefault(); });
```

Buttons and tap targets keep working: give them `touch-action:manipulation` (kills double-tap zoom, keeps taps instant).

## Scoping rule

Document-level `touchmove` prevention kills ALL native scrolling on the page. That is correct for full-screen games with no scrollable UI. If the page has scrollable regions (a level list, settings panel, chat log):

- Scope the prevention to the drag surface instead of the document:

```js
stage.addEventListener("touchmove", function(e){ e.preventDefault(); }, {passive:false});
```

- Give scrollable regions `touch-action:pan-y` so vertical scrolling still works there.

Never blanket-prevent on a page where the user needs to scroll somewhere.

## What not to do

- Do not rely on `touch-action:none` alone on the surface. Some webview containers still claim the gesture via page scroll/bounce; the fixed body + overscroll-behavior + touchmove prevention is the belt and suspenders that actually held.
- Do not use `position:fixed` on the body of a page that needs scrolling. This skill is for app-like, full-viewport pages only.

## QA checklist

- On a real phone, inside the actual bottom sheet: drag down hard on the game surface. The sheet must not move; the game must receive the drag.
- Drag in every direction on the surface, including fast flicks.
- Tap every button. Taps must still fire instantly (touch-action:manipulation, no 300ms delay).
- If the page has scrollable areas, scroll them. They must still scroll.
- Pinch on iOS. Nothing should zoom or escape to the sheet.
- 390px viewport, no console errors, no horizontal overflow.
