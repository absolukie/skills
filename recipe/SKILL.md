---
name: "recipe"
description: "Write Luke's recipes in the house recipe format and publish them to the recipes section at lukezhang.si/recipes/. Trigger on: 'recipe', 'add a recipe', 'write up this recipe', 'recipes section'."
---

# Recipe

## Purpose
Turn any recipe Luke wants kept (his own notes, a link, a photo of a cookbook page) into one page in the recipes section at lukezhang.si/recipes/, written in a single house format. One format for every recipe, so the collection reads as one shelf and any recipe can be cooked from at a glance.

## Rule zero: the format comes from the source post, never from habit
The house format is defined by one post: https://x.com/lexerlux/status/2111356462094315596 (shared by Luke 2026-10-17 with the instruction "write all recipes like this"). The format landed on 2026-10-17 and is codified in full below. Do not substitute a generic recipe layout (title, ingredients, numbered steps, notes) and call it his.

## Format source
Post by @LexerLux, 2026-10-17. Full text, verbatim: "i HATE how an engineer invented the correct way to write recipes like 20 years ago and nobody else ever used it"

The post's single image is a flowchart recipe chart for Banana Nut Bread, and the chart is the format. The parent agent read the post in Luke's signed-in managed browser on 2026-10-17 and confirmed the chart field by field. The rules below are that chart, codified. The specimen page (Banana Nut Bread, in the section) is the format's reference implementation.

## The format: one grid chart, no prose
- One chart per recipe. The whole recipe is the chart: a single grid on a pale-yellow rounded panel, thin green grid lines, plain black sans-serif type. The chart keeps these colors in both color schemes; it is a printed card, not themed interface.
- No prose anywhere in the recipe itself. No story, no headnote, no separate ingredient list, no numbered steps, no tips or substitutions inside the chart. The only text outside the chart on a recipe page is page furniture: the page heading, one short paragraph on the index only, and the format credit line.
- Title row: the recipe name in bold, servings in parentheses, for example "Banana Nut Bread (about 10 servings)".
- Setup rows: under the title, full-width rows hold anything that happens before ingredients combine, one instruction per row ("Butter and flour a loaf pan"; "Preheat oven to 350° F (170° C)").
- Columns read left to right as time:
  1. Ingredient column. Every ingredient is its own row, left-aligned, with dual quantities always: US first, metric in parentheses ("2 large (250 g) ripe bananas"; "6 Tbs. (90 mL) butter"; "1-1/3 cups (167 g) all-purpose flour"). An ingredient whose source gives no quantity stays quantity-free; never invent one.
  2. Prep column. The prep verb for that row's ingredient (mash; melt; lightly beat), blank where there is none. A prep shared by a stream of ingredients merges vertically across exactly those rows: "whisk" merged across all the dry-ingredient rows.
  3. Stage columns. Action cells after that. A stage cell merges vertically across exactly the rows it acts on, so combining is drawn, not described: a "mash until smooth" cell spans the banana, butter, and vanilla rows; a "fold" cell spans the eggs plus the dry rows. Final stages that act on everything are single full-height cells ("bake 350° F (170° C) 55 min."; "cool 10 min. in pan"; "cool on wire rack"). Action cell text is centered.
- Merged-cell spans carry the logic. Read a row left to right and you see everything that happens to that ingredient, in order. Read a column top to bottom and you see one moment in the cook.
- Cell text is terse: verb first, then the condition or the numbers that matter. Temperatures are always dual, Fahrenheit first with Celsius in parentheses. No sentences, no explanations.

## Rulings: adaptations for the collection (Kit, 2026-10-17, marked for Luke to strike)
The single chart is silent on the points below. Each is an adaptation, not part of the source format, and is marked so Luke can strike it.
- RULING, wide grids: when a recipe needs more stage columns than fit, the grid grows rightward and never wraps. On a phone the panel scrolls horizontally inside itself, with a subtle scroll hint; the page itself never overflows.
- RULING, sub-recipes: a recipe with a sub-recipe gets a second complete chart below the main chart, under its own title row. In the main chart the sub-recipe appears as one ingredient row named for it, with its yield as the quantity. Never nest a chart inside a cell.
- RULING, print: a print stylesheet fits the whole chart on one landscape page, keeps the yellow panel and the green lines (print-color-adjust: exact), and drops the page furniture and the scroll behavior.
- RULING, web interaction: tapping an ingredient row on the web page highlights that ingredient's full path across the stages; a second tap clears it. A print chart cannot do this; the web page may, because the highlight teaches the reading rule.

## Intake: how a recipe arrives
A recipe can start from any of these, and the intake job is the same: get a complete, faithful source text before any formatting happens.
1. Luke's own notes, in any shape. Ask for nothing that is missing by inventing it; a missing quantity stays missing and gets flagged on the page or asked about, never guessed.
2. A link. Fetch the page text and extract the recipe as written, including its quantities, order, and timing. Credit the source on the page.
3. A photo of a cookbook page or a handwritten card. Transcribe it exactly first, then format the transcription. Keep the transcription with the draft so errors can be checked against the photo.

Drafts live in ~/workspace/blog-drafts/recipes/<slug>/ following the blog draft pattern, one folder per recipe.

## Publishing
- Section: lukezhang.si/recipes/ in the absolukie/lukezhang-si repo, index plus one page per recipe at /recipes/<slug>/, following the blog and primers house pattern.
- Page style matches the primer shell family: math-cute, phone-first, readable in light and dark schemes. The chart itself keeps its print colors in both schemes, per the format above.
- Ship surgically (single-file pushes, compare-and-swap), never a full-tree push. Live means the served URL verified: HTTP 200, served bytes equal local bytes plus the standard 248-byte beacon delta.
- The first page in the section is the specimen: the recipe from the lexerlux post itself, rebuilt in the format it demonstrates, credited on the page as the format's source with a link to the post.
- Do not invent personal recipes of Luke's to fill the shelf. One honest specimen beats a padded section.
- Public pages carry no sensitive information, ever, and never name Gabrielle.

## QA checks for a recipe page
- Format: the page follows the house format exactly as codified above. Any deviation is a defect, not a style choice.
- Fidelity: every quantity, time, temperature, and step order matches the source text from intake. A second read of the source against the page is the check.
- Mechanics: zero em dashes and zero en dashes anywhere on the page. Tag balance parses clean. Every inline script passes `node --check`.
- Rendering: quick rendered check at 390x844 in both color schemes, computed styles confirmed, no horizontal overflow, no page errors.
- Live: after shipping, the served page returns 200 and byte-matches local plus the beacon delta. Never declare live on the first check; purge and re-check if stale.
