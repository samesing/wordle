# Wordle: Python program to solve Wordle puzzle

After nearly three years of playing Wordle, I finally hit the elusive milestone last month: solving it on the very first guess. Elated, I almost retired on the spot (for about 10 seconds) before moving on to my next daily puzzle (Connections).

But the moment sparked an idea. I decided to run a little experiment. A tripartite Wordle race between:

- Myself

- A Python-based program I wrote, and

- ChatGPT.

The goal? To explore how human intuition, algorithmic logic, and AI language models compare when playing the same constraint-based puzzle.

Who do you think will win — human, code, or AI?

# How to run the code?
The python file "wordle prompt.py" is the main interface code. When run, it asks for two initial inputs -- a seed word (the first guess; to ensure fair comparison, I ensured that the first word guess is same for everyone) and the feedback for this word. It needs to be in a 5 character format like ygxxxy where y = yellow, g = green and x = gray.
