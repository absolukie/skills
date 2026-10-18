---
name: verify-tiny-learning-lab
description: "Verify the Tiny Learning Lab (projects.lukezhang.si/tiny-learning-lab/): five tiny problems solved three ways each in one self-contained page (XOR trainers, rock paper scissors learners, a three-ranker search engine, Monty Hall strategies, maze dot). Feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: Tiny Learning Lab

Live URL: https://projects.lukezhang.si/tiny-learning-lab/
Source: ~/workspace/tiny-learning-lab/index.html (single self-contained file; deploy by surgical overlay to sites/tiny-learning-lab/index.html in absolukie/lukezhang-si, plus the "tiny-learning-lab" entry in worker.js SITES)

Feature map: ~/workspace/tiny-learning-lab/verify/FEATURE_MAP.md
Harness: ~/workspace/tiny-learning-lab/verify/harness.py
Last report: ~/workspace/tiny-learning-lab/verify/REPORT.md

Run locally: `python3 ~/workspace/tiny-learning-lab/verify/harness.py`

The harness drives the real UI at 390x844: page health (title, no overflow, 16px search input, no em or en dashes in rendered text); the XOR race (perceptron stuck at 3 of 4 or below after 100 epochs, the RNN at seed 36 (Adam; its backpropagation-through-time gradients were numeric-checked at build time, worst relative error 0.00000005) and the tiny transformer at seed 7 both at 4 of 4 within 100 epochs, training now animated in batches so the waits poll for the finished epoch count before reading the final score, attention bars summing to 100, reset zeroing epochs); the perceptron upgrade (the Add a hidden layer button starts hidden, appears once the plain perceptron reaches 100 failed epochs, resets and retitles the lane on tap, and the upgraded 2-2-1 model reaches 4 of 4 with its 9 parameters shown); the See everything panels (each lane's panel starts hidden, opens on tap, and shows every parameter: perceptron w and b, RNN all 19 with Wx and Wh plus the state after each bit for all 4 inputs, transformer all 113 with Wk and Wh plus attention rows for all 4 inputs; the RNN panel's numbers provably change after one Train 1 step); rock paper scissors (three opponents each scoring all 6 rock rounds, pattern line, reset); the search engine (default "moon cat" crowns the stuffer page under keyword count and "The Moon Cat" under TF-IDF and BM25, chips switching queries, 4 rows per ranker); Monty Hall (one round narrating doors and car, rates within 10 points of 33 / 67 / 50 after 1001 rounds, reset); the maze (56 cells per board, planner at 13 steps, Q-learning at 13 steps after 200 episodes, random walk reporting a step count); zero page errors.

Design notes that matter for re-verification: the transformer lane's gradients were checked against numeric gradients during the build (worst relative error 0.00000), and its head sees the attention blend plus the mean of the two token vectors as a residual; without that residual most random inits stall at 3 of 4. The random walk cap is 2000 steps, at which it reliably reaches the goal in a few hundred steps; the contrast is step count, not failure.
